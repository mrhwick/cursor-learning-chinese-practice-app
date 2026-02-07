from __future__ import annotations

import secrets
from typing import Optional

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .auth import SESSION_USER_ID_KEY, hash_password, require_teacher, require_user, verify_password
from .config import get_settings
from .db import Base, engine, get_db
from .models import Classroom, Enrollment, Feedback, ModelAudio, Phrase, Submission, User
from .schemas import (
    AuthLoginRequest,
    AuthSignupRequest,
    ClassroomCreateRequest,
    ClassroomPublic,
    FeedbackCreateRequest,
    FeedbackPublic,
    HealthResponse,
    JoinClassroomRequest,
    PhraseCreateRequest,
        PhraseUpdateRequest,
    PhrasePublic,
    SubmissionPublic,
    UserPublic,
)
from .storage import UploadValidationError, store_upload


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title="Chinese Practice Studio API")

    # In dev, we rely on Vite proxying /api to this server (same-origin),
    # but CORS is still helpful for direct API calls.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)

    @app.get("/api/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(ok=True)

    @app.get("/api/phrases", response_model=list[PhrasePublic])
    def list_my_phrases(
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> list[PhrasePublic]:
        classroom_ids = (
            db.execute(select(Enrollment.classroom_id).where(Enrollment.user_id == user.id)).scalars().all()
        )
        if not classroom_ids:
            return []
        phrases = (
            db.execute(
                select(Phrase)
                .where(Phrase.classroom_id.in_(classroom_ids))
                .order_by(Phrase.created_at.desc())
            )
            .scalars()
            .all()
        )
        out: list[PhrasePublic] = []
        for p in phrases:
            out.append(
                PhrasePublic(
                    id=p.id,
                    classroom_id=p.classroom_id,
                    chinese=p.chinese,
                    pinyin=p.pinyin,
                    english=p.english,
                    notes=p.notes,
                    created_at=p.created_at,
                    has_model_audio=p.model_audio is not None,
                )
            )
        return out

    @app.post("/api/auth/signup", response_model=UserPublic)
    def signup(payload: AuthSignupRequest, request: Request, db: Session = Depends(get_db)) -> UserPublic:
        existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        try:
            password_hash = hash_password(payload.password)
        except Exception:
            # If the crypto backend isn't installed correctly, fail with a friendly message
            # instead of a 500 stack trace.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password hashing failed. Try reinstalling API dependencies (see docs/TROUBLESHOOTING.md).",
            )
        user = User(email=payload.email, password_hash=password_hash, role=payload.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        request.session[SESSION_USER_ID_KEY] = user.id
        return UserPublic(id=user.id, email=user.email, role=user.role)

    @app.post("/api/auth/login", response_model=UserPublic)
    def login(payload: AuthLoginRequest, request: Request, db: Session = Depends(get_db)) -> UserPublic:
        user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        request.session[SESSION_USER_ID_KEY] = user.id
        return UserPublic(id=user.id, email=user.email, role=user.role)

    @app.post("/api/auth/logout")
    def logout(request: Request) -> dict:
        request.session.pop(SESSION_USER_ID_KEY, None)
        return {"ok": True}

    @app.get("/api/me", response_model=UserPublic)
    def me(user: User = Depends(require_user)) -> UserPublic:
        return UserPublic(id=user.id, email=user.email, role=user.role)

    @app.post("/api/classrooms", response_model=ClassroomPublic)
    def create_classroom(
        payload: ClassroomCreateRequest,
        db: Session = Depends(get_db),
        teacher: User = Depends(require_teacher),
    ) -> ClassroomPublic:
        invite_code = secrets.token_urlsafe(6)
        classroom = Classroom(name=payload.name, invite_code=invite_code, owner_id=teacher.id)
        db.add(classroom)
        db.commit()
        db.refresh(classroom)

        # Owner is also enrolled.
        enrollment = Enrollment(user_id=teacher.id, classroom_id=classroom.id)
        db.add(enrollment)
        db.commit()

        return ClassroomPublic(
            id=classroom.id,
            name=classroom.name,
            invite_code=classroom.invite_code,
            owner_id=classroom.owner_id,
            created_at=classroom.created_at,
        )

    @app.get("/api/classrooms", response_model=list[ClassroomPublic])
    def list_my_classrooms(
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> list[ClassroomPublic]:
        classroom_ids = (
            db.execute(select(Enrollment.classroom_id).where(Enrollment.user_id == user.id)).scalars().all()
        )
        if not classroom_ids:
            return []
        classrooms = (
            db.execute(select(Classroom).where(Classroom.id.in_(classroom_ids)).order_by(Classroom.created_at.desc()))
            .scalars()
            .all()
        )
        return [
            ClassroomPublic(
                id=c.id,
                name=c.name,
                invite_code=c.invite_code,
                owner_id=c.owner_id,
                created_at=c.created_at,
            )
            for c in classrooms
        ]

    @app.post("/api/classrooms/join")
    def join_classroom(
        payload: JoinClassroomRequest,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> dict:
        classroom = db.execute(select(Classroom).where(Classroom.invite_code == payload.invite_code)).scalar_one_or_none()
        if not classroom:
            raise HTTPException(status_code=404, detail="Invite code not found")

        existing = db.execute(
            select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.classroom_id == classroom.id)
        ).scalar_one_or_none()
        if existing:
            return {"ok": True, "classroom_id": classroom.id}

        db.add(Enrollment(user_id=user.id, classroom_id=classroom.id))
        db.commit()
        return {"ok": True, "classroom_id": classroom.id}

    def _require_enrolled(db: Session, user_id: int, classroom_id: int) -> None:
        enrollment = db.execute(
            select(Enrollment).where(Enrollment.user_id == user_id, Enrollment.classroom_id == classroom_id)
        ).scalar_one_or_none()
        if not enrollment:
            raise HTTPException(status_code=403, detail="Not enrolled in this classroom")

    @app.get("/api/classrooms/{classroom_id}/phrases", response_model=list[PhrasePublic])
    def list_phrases(
        classroom_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> list[PhrasePublic]:
        _require_enrolled(db, user.id, classroom_id)
        phrases = db.execute(select(Phrase).where(Phrase.classroom_id == classroom_id).order_by(Phrase.created_at.desc())).scalars().all()
        out: list[PhrasePublic] = []
        for p in phrases:
            out.append(
                PhrasePublic(
                    id=p.id,
                    classroom_id=p.classroom_id,
                    chinese=p.chinese,
                    pinyin=p.pinyin,
                    english=p.english,
                    notes=p.notes,
                    created_at=p.created_at,
                    has_model_audio=p.model_audio is not None,
                )
            )
        return out

    @app.post("/api/classrooms/{classroom_id}/phrases", response_model=PhrasePublic)
    def create_phrase(
        classroom_id: int,
        payload: PhraseCreateRequest,
        db: Session = Depends(get_db),
        teacher: User = Depends(require_teacher),
    ) -> PhrasePublic:
        _require_enrolled(db, teacher.id, classroom_id)
        classroom = db.get(Classroom, classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")
        if classroom.owner_id != teacher.id:
            raise HTTPException(status_code=403, detail="Only the classroom owner can create phrases")
        phrase = Phrase(
            classroom_id=classroom_id,
            chinese=payload.chinese,
            pinyin=payload.pinyin,
            english=payload.english,
            notes=payload.notes,
        )
        db.add(phrase)
        db.commit()
        db.refresh(phrase)
        return PhrasePublic(
            id=phrase.id,
            classroom_id=phrase.classroom_id,
            chinese=phrase.chinese,
            pinyin=phrase.pinyin,
            english=phrase.english,
            notes=phrase.notes,
            created_at=phrase.created_at,
            has_model_audio=False,
        )

    @app.get("/api/phrases/{phrase_id}", response_model=PhrasePublic)
    def get_phrase(
        phrase_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> PhrasePublic:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)
        return PhrasePublic(
            id=phrase.id,
            classroom_id=phrase.classroom_id,
            chinese=phrase.chinese,
            pinyin=phrase.pinyin,
            english=phrase.english,
            notes=phrase.notes,
            created_at=phrase.created_at,
            has_model_audio=phrase.model_audio is not None,
        )

    @app.put("/api/phrases/{phrase_id}", response_model=PhrasePublic)
    def update_phrase(
        phrase_id: int,
        payload: PhraseUpdateRequest,
        db: Session = Depends(get_db),
        teacher: User = Depends(require_teacher),
    ) -> PhrasePublic:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        classroom = db.get(Classroom, phrase.classroom_id)
        if not classroom or classroom.owner_id != teacher.id:
            raise HTTPException(status_code=403, detail="Only the classroom owner can edit phrases")
        phrase.chinese = payload.chinese
        phrase.pinyin = payload.pinyin
        phrase.english = payload.english
        phrase.notes = payload.notes
        db.commit()
        db.refresh(phrase)
        return PhrasePublic(
            id=phrase.id,
            classroom_id=phrase.classroom_id,
            chinese=phrase.chinese,
            pinyin=phrase.pinyin,
            english=phrase.english,
            notes=phrase.notes,
            created_at=phrase.created_at,
            has_model_audio=phrase.model_audio is not None,
        )

    @app.delete("/api/phrases/{phrase_id}")
    def delete_phrase(
        phrase_id: int,
        db: Session = Depends(get_db),
        teacher: User = Depends(require_teacher),
    ) -> dict:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        classroom = db.get(Classroom, phrase.classroom_id)
        if not classroom or classroom.owner_id != teacher.id:
            raise HTTPException(status_code=403, detail="Only the classroom owner can delete phrases")
        db.delete(phrase)
        db.commit()
        return {"ok": True}

    @app.post("/api/phrases/{phrase_id}/model-audio")
    def upload_model_audio(
        phrase_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        teacher: User = Depends(require_teacher),
    ) -> dict:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        classroom = db.get(Classroom, phrase.classroom_id)
        if not classroom or classroom.owner_id != teacher.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        try:
            stored = store_upload(
                file,
                subdir=f"model_audio/{phrase.classroom_id}/{phrase.id}",
                max_bytes=20 * 1024 * 1024,
                require_content_type_prefix="audio/",
            )
        except UploadValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        existing = db.execute(select(ModelAudio).where(ModelAudio.phrase_id == phrase.id)).scalar_one_or_none()
        if existing:
            existing.storage_path = stored.storage_path
            existing.original_filename = stored.original_filename
            existing.content_type = stored.content_type
            db.commit()
        else:
            db.add(
                ModelAudio(
                    phrase_id=phrase.id,
                    storage_path=stored.storage_path,
                    original_filename=stored.original_filename,
                    content_type=stored.content_type,
                )
            )
            db.commit()
        return {"ok": True}

    @app.get("/api/phrases/{phrase_id}/model-audio")
    def get_model_audio(
        phrase_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ):
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)
        model = db.execute(select(ModelAudio).where(ModelAudio.phrase_id == phrase.id)).scalar_one_or_none()
        if not model:
            raise HTTPException(status_code=404, detail="No model audio")
        return FileResponse(path=model.storage_path, media_type=model.content_type, filename=model.original_filename)

    @app.post("/api/phrases/{phrase_id}/submissions", response_model=SubmissionPublic)
    def create_submission(
        phrase_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> SubmissionPublic:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)
        try:
            stored = store_upload(
                file,
                subdir=f"submissions/{phrase.classroom_id}/{phrase.id}/{user.id}",
                max_bytes=20 * 1024 * 1024,
                require_content_type_prefix="audio/",
            )
        except UploadValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        submission = Submission(
            phrase_id=phrase.id,
            user_id=user.id,
            storage_path=stored.storage_path,
            original_filename=stored.original_filename,
            content_type=stored.content_type,
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return SubmissionPublic(id=submission.id, phrase_id=submission.phrase_id, user_id=submission.user_id, created_at=submission.created_at)

    @app.get("/api/phrases/{phrase_id}/submissions", response_model=list[SubmissionPublic])
    def list_submissions(
        phrase_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> list[SubmissionPublic]:
        phrase = db.get(Phrase, phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)
        subs = db.execute(select(Submission).where(Submission.phrase_id == phrase.id).order_by(Submission.created_at.desc())).scalars().all()
        return [SubmissionPublic(id=s.id, phrase_id=s.phrase_id, user_id=s.user_id, created_at=s.created_at) for s in subs]

    @app.get("/api/submissions/{submission_id}/audio")
    def get_submission_audio(
        submission_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ):
        sub = db.get(Submission, submission_id)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        phrase = db.get(Phrase, sub.phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)
        return FileResponse(path=sub.storage_path, media_type=sub.content_type, filename=sub.original_filename)

    @app.post("/api/submissions/{submission_id}/feedback", response_model=FeedbackPublic)
    def leave_feedback(
        submission_id: int,
        payload: FeedbackCreateRequest,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> FeedbackPublic:
        sub = db.get(Submission, submission_id)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        phrase = db.get(Phrase, sub.phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)

        fb = Feedback(
            submission_id=sub.id,
            author_id=user.id,
            comment=payload.comment,
            score_tones=payload.score_tones,
            score_clarity=payload.score_clarity,
        )
        db.add(fb)
        db.commit()
        db.refresh(fb)
        return FeedbackPublic(
            id=fb.id,
            submission_id=fb.submission_id,
            author_id=fb.author_id,
            comment=fb.comment,
            score_tones=fb.score_tones,
            score_clarity=fb.score_clarity,
            created_at=fb.created_at,
        )

    @app.get("/api/submissions/{submission_id}/feedback", response_model=list[FeedbackPublic])
    def list_feedback(
        submission_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> list[FeedbackPublic]:
        sub = db.get(Submission, submission_id)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        phrase = db.get(Phrase, sub.phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        _require_enrolled(db, user.id, phrase.classroom_id)

        items = db.execute(select(Feedback).where(Feedback.submission_id == sub.id).order_by(Feedback.created_at.asc())).scalars().all()
        return [
            FeedbackPublic(
                id=f.id,
                submission_id=f.submission_id,
                author_id=f.author_id,
                comment=f.comment,
                score_tones=f.score_tones,
                score_clarity=f.score_clarity,
                created_at=f.created_at,
            )
            for f in items
        ]

    @app.delete("/api/feedback/{feedback_id}")
    def delete_feedback(
        feedback_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(require_user),
    ) -> dict:
        fb = db.get(Feedback, feedback_id)
        if not fb:
            raise HTTPException(status_code=404, detail="Feedback not found")
        sub = db.get(Submission, fb.submission_id)
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        phrase = db.get(Phrase, sub.phrase_id)
        if not phrase:
            raise HTTPException(status_code=404, detail="Phrase not found")
        classroom = db.get(Classroom, phrase.classroom_id)
        if not classroom:
            raise HTTPException(status_code=404, detail="Classroom not found")

        _require_enrolled(db, user.id, phrase.classroom_id)

        is_author = user.id == fb.author_id
        is_teacher_owner = user.role == "teacher" and classroom.owner_id == user.id
        if not (is_author or is_teacher_owner):
            raise HTTPException(status_code=403, detail="Not allowed")

        db.delete(fb)
        db.commit()
        return {"ok": True}

    return app


app = create_app()

