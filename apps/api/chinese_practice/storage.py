from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile

from .config import get_settings


@dataclass(frozen=True)
class StoredFile:
    storage_path: str
    original_filename: str
    content_type: str


class UploadValidationError(Exception):
    pass


def _safe_ext(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext and len(ext) <= 10:
        return ext
    return ""


def store_upload(
    upload: UploadFile,
    subdir: str,
    *,
    max_bytes: int = 10 * 1024 * 1024,
    require_content_type_prefix: str | None = None,
) -> StoredFile:
    settings = get_settings()
    base = Path(settings.upload_dir)
    target_dir = base / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    if require_content_type_prefix:
        ct = upload.content_type or ""
        if not ct.startswith(require_content_type_prefix):
            raise UploadValidationError(f"Invalid content type: {ct or '(missing)'}")

    token = secrets.token_urlsafe(16)
    ext = _safe_ext(upload.filename or "")
    filename = f"{token}{ext}"
    path = target_dir / filename

    total = 0
    with path.open("wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise UploadValidationError(f"File too large (max {max_bytes} bytes)")
            f.write(chunk)

    return StoredFile(
        storage_path=str(path),
        original_filename=upload.filename or "upload",
        content_type=upload.content_type or "application/octet-stream",
    )

