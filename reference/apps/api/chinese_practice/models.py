from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)  # "teacher" | "student"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    classrooms_owned: Mapped[list["Classroom"]] = relationship(back_populates="owner")


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    invite_code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    owner: Mapped[User] = relationship(back_populates="classrooms_owned")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="classroom")
    phrases: Mapped[list["Phrase"]] = relationship(back_populates="classroom")


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (UniqueConstraint("user_id", "classroom_id", name="uq_enrollment_user_classroom"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship()
    classroom: Mapped[Classroom] = relationship(back_populates="enrollments")


class Phrase(Base):
    __tablename__ = "phrases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"), nullable=False, index=True)

    chinese: Mapped[str] = mapped_column(String(500), nullable=False)
    pinyin: Mapped[str] = mapped_column(String(500), nullable=False)
    english: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    classroom: Mapped[Classroom] = relationship(back_populates="phrases")
    model_audio: Mapped[Optional["ModelAudio"]] = relationship(back_populates="phrase", uselist=False)
    submissions: Mapped[list["Submission"]] = relationship(back_populates="phrase")


class ModelAudio(Base):
    __tablename__ = "model_audio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phrase_id: Mapped[int] = mapped_column(ForeignKey("phrases.id"), unique=True, nullable=False, index=True)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    phrase: Mapped[Phrase] = relationship(back_populates="model_audio")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phrase_id: Mapped[int] = mapped_column(ForeignKey("phrases.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    phrase: Mapped[Phrase] = relationship(back_populates="submissions")
    user: Mapped[User] = relationship()
    feedback: Mapped[list["Feedback"]] = relationship(back_populates="submission")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    comment: Mapped[str] = mapped_column(Text, nullable=False)
    score_tones: Mapped[int] = mapped_column(Integer, nullable=False)
    score_clarity: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    submission: Mapped[Submission] = relationship(back_populates="feedback")
    author: Mapped[User] = relationship()

