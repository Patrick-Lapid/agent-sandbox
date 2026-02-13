import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class PriorityEnum(str, enum.Enum):
    """Priority levels for cards."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Card(Base):
    """Card model representing a task card within a list."""

    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    position = Column(Integer, nullable=False, default=0)
    list_id = Column(UUID(as_uuid=True), ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    assigned_to_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(Enum(PriorityEnum), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    list = relationship("List", back_populates="cards")
    assigned_to = relationship("User", back_populates="assigned_cards", foreign_keys=[assigned_to_id])
