from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class BoardBase(BaseModel):
    """Base board schema with common attributes."""
    title: Optional[str] = None
    description: Optional[str] = None


class BoardCreate(BaseModel):
    """Schema for creating a new board."""
    title: str
    description: Optional[str] = None


class BoardUpdate(BaseModel):
    """Schema for updating a board."""
    title: Optional[str] = None
    description: Optional[str] = None


class BoardResponse(BaseModel):
    """Schema for board response."""
    id: UUID
    title: str
    description: Optional[str] = None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardDetail(BoardResponse):
    """Schema for detailed board response with nested lists and cards."""
    from app.schemas.list import ListDetail

    lists: List[ListDetail] = []

    model_config = ConfigDict(from_attributes=True)
