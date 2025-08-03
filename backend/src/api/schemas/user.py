import uuid

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str | None = None
    password: str | None = None


class UserOut(BaseModel):
    id: uuid.UUID | None = None
    username: str | None = None
