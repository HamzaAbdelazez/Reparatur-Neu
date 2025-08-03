import uuid
from datetime import datetime, UTC
from typing import List

from sqlalchemy import String, LargeBinary, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(length=255), nullable=False)

    uploaded_pdfs: Mapped[List["UploadedPdf"]] = relationship("UploadedPdf", back_populates="user")


class UploadedPdf(Base):
    __tablename__ = "uploaded_pdfs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(length=255), nullable=False)
    content: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # Store actual PDF file content as binary data
    file_size: Mapped[int] = mapped_column(Integer)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="uploaded_pdfs")
