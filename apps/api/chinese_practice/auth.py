from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import get_db
from .models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_USER_ID_KEY = "user_id"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get(SESSION_USER_ID_KEY)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    return user


def require_teacher(user: User = Depends(require_user)) -> User:
    if user.role != "teacher":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher role required")
    return user

