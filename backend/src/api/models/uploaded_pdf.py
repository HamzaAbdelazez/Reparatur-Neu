from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UploadedPdfIn(BaseModel):
    user_id: UUID
    title: str
    content: bytes
    file_size: int | None = None


class UploadedPdfOut(BaseModel):
    id: UUID
    title: str
    uploaded_at: datetime
    file_size: int | None = None
    user_id: UUID
