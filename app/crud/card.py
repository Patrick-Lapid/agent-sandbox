from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


class CRUDCard(CRUDBase[Card, CardCreate, CardUpdate]):
    """CRUD operations for Card model."""

    def create_in_list(
        self, db: Session, *, obj_in: CardCreate, list_id: UUID
    ) -> Card:
        """
        Create a new card in a list.

        Args:
            db: Database session
            obj_in: Card creation schema
            list_id: Parent list ID

        Returns:
            Created card instance
        """
        db_obj = Card(
            title=obj_in.title,
            description=obj_in.description,
            position=obj_in.position,
            list_id=list_id,
            assigned_to_id=obj_in.assigned_to_id,
            due_date=obj_in.due_date,
            priority=obj_in.priority
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_list(
        self, db: Session, *, list_id: UUID
    ) -> List[Card]:
        """
        Get all cards in a list, ordered by position.

        Args:
            db: Database session
            list_id: List ID

        Returns:
            List of card instances
        """
        return (
            db.query(Card)
            .filter(Card.list_id == list_id)
            .order_by(Card.position)
            .all()
        )

    def move_to_list(
        self, db: Session, *, db_obj: Card, list_id: UUID, position: int
    ) -> Card:
        """
        Move card to a different list.

        Args:
            db: Database session
            db_obj: Card instance
            list_id: Target list ID
            position: Position in target list

        Returns:
            Updated card instance
        """
        db_obj.list_id = list_id
        db_obj.position = position
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def reorder(
        self, db: Session, *, db_obj: Card, new_position: int
    ) -> Card:
        """
        Update card position within the same list.

        Args:
            db: Database session
            db_obj: Card instance
            new_position: New position value

        Returns:
            Updated card instance
        """
        db_obj.position = new_position
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


card = CRUDCard(Card)
