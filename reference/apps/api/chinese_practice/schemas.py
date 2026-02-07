from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class HealthResponse(BaseModel):
    ok: bool


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str


class AuthSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=200)
    role: str = Field(pattern="^(teacher|student)$")


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClassroomCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class ClassroomPublic(BaseModel):
    id: int
    name: str
    invite_code: str
    owner_id: int
    created_at: datetime


class JoinClassroomRequest(BaseModel):
    invite_code: str = Field(min_length=4, max_length=32)


class PhraseCreateRequest(BaseModel):
    chinese: str = Field(min_length=1, max_length=500)
    pinyin: str = Field(min_length=1, max_length=500)
    english: str = Field(min_length=1, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=5000)


class PhraseUpdateRequest(PhraseCreateRequest):
    pass


class PhrasePublic(BaseModel):
    id: int
    classroom_id: int
    chinese: str
    pinyin: str
    english: str
    notes: Optional[str]
    created_at: datetime
    has_model_audio: bool


class SubmissionPublic(BaseModel):
    id: int
    phrase_id: int
    user_id: int
    created_at: datetime


class FeedbackCreateRequest(BaseModel):
    comment: str = Field(min_length=1, max_length=5000)
    score_tones: int = Field(ge=1, le=5)
    score_clarity: int = Field(ge=1, le=5)


class FeedbackPublic(BaseModel):
    id: int
    submission_id: int
    author_id: int
    comment: str
    score_tones: int
    score_clarity: int
    created_at: datetime

