from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.board import board as board_crud
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse, BoardDetail
from app.models.user import User
from app.models.board import Board

router = APIRouter()


@router.get("/", response_model=List[BoardResponse])
def list_boards(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> List[Board]:
    """
    Get all boards owned by current user.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user

    Returns:
        List of user's boards
    """
    boards = board_crud.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return boards


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    *,
    db: Session = Depends(get_db),
    board_in: BoardCreate,
    current_user: User = Depends(get_current_active_user)
) -> Board:
    """
    Create a new board.

    Args:
        db: Database session
        board_in: Board creation data
        current_user: Current authenticated user

    Returns:
        Created board
    """
    board = board_crud.create_with_owner(
        db, obj_in=board_in, owner_id=current_user.id
    )
    return board


@router.get("/{board_id}", response_model=BoardDetail)
def get_board(
    *,
    db: Session = Depends(get_db),
    board_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> Board:
    """
    Get board by ID with all lists and cards.

    Args:
        db: Database session
        board_id: Board ID
        current_user: Current authenticated user

    Returns:
        Board with nested lists and cards

    Raises:
        HTTPException: If board not found or user doesn't own it
    """
    board = board_crud.get_with_details(db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    # Check ownership
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this board"
        )

    return board


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    *,
    db: Session = Depends(get_db),
    board_id: UUID,
    board_in: BoardUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Board:
    """
    Update board.

    Args:
        db: Database session
        board_id: Board ID
        board_in: Board update data
        current_user: Current authenticated user

    Returns:
        Updated board

    Raises:
        HTTPException: If board not found or user doesn't own it
    """
    board = board_crud.get(db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    # Check ownership
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this board"
        )

    board = board_crud.update(db, db_obj=board, obj_in=board_in)
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    *,
    db: Session = Depends(get_db),
    board_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete board (and all its lists and cards via cascade).

    Args:
        db: Database session
        board_id: Board ID
        current_user: Current authenticated user

    Raises:
        HTTPException: If board not found or user doesn't own it
    """
    board = board_crud.get(db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    # Check ownership
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this board"
        )

    board_crud.remove(db, id=board_id)
