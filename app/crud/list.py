from typing import List as TypeList, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.list import List
from app.schemas.list import ListCreate, ListUpdate


class CRUDList(CRUDBase[List, ListCreate, ListUpdate]):
    """CRUD operations for List model."""

    def create_in_board(
        self, db: Session, *, obj_in: ListCreate, board_id: UUID
    ) -> List:
        """
        Create a new list in a board.

        Args:
            db: Database session
            obj_in: List creation schema
            board_id: Parent board ID

        Returns:
            Created list instance
        """
        db_obj = List(
            title=obj_in.title,
            position=obj_in.position,
            board_id=board_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_board(
        self, db: Session, *, board_id: UUID
    ) -> TypeList[List]:
        """
        Get all lists in a board, ordered by position.

        Args:
            db: Database session
            board_id: Board ID

        Returns:
            List of list instances
        """
        return (
            db.query(List)
            .filter(List.board_id == board_id)
            .order_by(List.position)
            .all()
        )

    def reorder(
        self, db: Session, *, db_obj: List, new_position: int
    ) -> List:
        """
        Update list position.

        Args:
            db: Database session
            db_obj: List instance
            new_position: New position value

        Returns:
            Updated list instance
        """
        db_obj.position = new_position
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


list_crud = CRUDList(List)
