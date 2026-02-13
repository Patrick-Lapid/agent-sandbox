from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


class CRUDBoard(CRUDBase[Board, BoardCreate, BoardUpdate]):
    """CRUD operations for Board model."""

    def create_with_owner(
        self, db: Session, *, obj_in: BoardCreate, owner_id: UUID
    ) -> Board:
        """
        Create a new board with owner.

        Args:
            db: Database session
            obj_in: Board creation schema
            owner_id: Owner user ID

        Returns:
            Created board instance
        """
        db_obj = Board(
            title=obj_in.title,
            description=obj_in.description,
            owner_id=owner_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Board]:
        """
        Get all boards owned by a specific user.

        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of board instances
        """
        return (
            db.query(Board)
            .filter(Board.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_details(self, db: Session, *, id: UUID) -> Optional[Board]:
        """
        Get board with all nested lists and cards.

        Args:
            db: Database session
            id: Board ID

        Returns:
            Board instance with lists and cards loaded, None if not found
        """
        return (
            db.query(Board)
            .filter(Board.id == id)
            .options(
                joinedload(Board.lists).joinedload("cards")
            )
            .first()
        )


board = CRUDBoard(Board)
