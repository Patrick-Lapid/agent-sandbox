from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.card import PriorityEnum


class CardBase(BaseModel):
    """Base card schema with common attributes."""
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None


class CardCreate(BaseModel):
    """Schema for creating a new card."""
    title: str
    description: Optional[str] = None
    position: int = 0
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None


class CardUpdate(BaseModel):
    """Schema for updating a card."""
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None


class CardMove(BaseModel):
    """Schema for moving a card to a different list."""
    list_id: UUID
    position: int = 0


class CardReorder(BaseModel):
    """Schema for reordering a card within the same list."""
    position: int


class CardResponse(BaseModel):
    """Schema for card response."""
    id: UUID
    title: str
    description: Optional[str] = None
    position: int
    list_id: UUID
    assigned_to_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
