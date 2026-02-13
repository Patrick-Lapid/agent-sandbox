from pydantic import BaseModel, ConfigDict
from typing import Optional, List as TypeList
from uuid import UUID
from datetime import datetime


class ListBase(BaseModel):
    """Base list schema with common attributes."""
    title: Optional[str] = None
    position: Optional[int] = None


class ListCreate(BaseModel):
    """Schema for creating a new list."""
    title: str
    position: int = 0


class ListUpdate(BaseModel):
    """Schema for updating a list."""
    title: Optional[str] = None
    position: Optional[int] = None


class ListReorder(BaseModel):
    """Schema for reordering a list."""
    position: int


class ListResponse(BaseModel):
    """Schema for list response."""
    id: UUID
    title: str
    position: int
    board_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ListDetail(ListResponse):
    """Schema for detailed list response with nested cards."""
    from app.schemas.card import CardResponse

    cards: TypeList[CardResponse] = []

    model_config = ConfigDict(from_attributes=True)
