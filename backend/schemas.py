from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class NoteCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )
    content: str = Field(
        min_length=1,
    )

class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
