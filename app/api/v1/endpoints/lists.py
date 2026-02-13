from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.board import board as board_crud
from app.crud.list import list_crud
from app.schemas.list import ListCreate, ListUpdate, ListResponse, ListReorder
from app.models.user import User
from app.models.list import List

router = APIRouter()


@router.post("/boards/{board_id}/lists/", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(
    *,
    db: Session = Depends(get_db),
    board_id: UUID,
    list_in: ListCreate,
    current_user: User = Depends(get_current_active_user)
) -> List:
    """
    Create a new list in a board.

    Args:
        db: Database session
        board_id: Parent board ID
        list_in: List creation data
        current_user: Current authenticated user

    Returns:
        Created list

    Raises:
        HTTPException: If board not found or user doesn't own it
    """
    # Check if board exists and user owns it
    board = board_crud.get(db, id=board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )

    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this board"
        )

    # Create list
    list_obj = list_crud.create_in_board(db, obj_in=list_in, board_id=board_id)
    return list_obj


@router.get("/lists/{list_id}", response_model=ListResponse)
def get_list(
    *,
    db: Session = Depends(get_db),
    list_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> List:
    """
    Get list by ID.

    Args:
        db: Database session
        list_id: List ID
        current_user: Current authenticated user

    Returns:
        List

    Raises:
        HTTPException: If list not found or user doesn't own parent board
    """
    list_obj = list_crud.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

    # Check board ownership
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this list"
        )

    return list_obj


@router.put("/lists/{list_id}", response_model=ListResponse)
def update_list(
    *,
    db: Session = Depends(get_db),
    list_id: UUID,
    list_in: ListUpdate,
    current_user: User = Depends(get_current_active_user)
) -> List:
    """
    Update list.

    Args:
        db: Database session
        list_id: List ID
        list_in: List update data
        current_user: Current authenticated user

    Returns:
        Updated list

    Raises:
        HTTPException: If list not found or user doesn't own parent board
    """
    list_obj = list_crud.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

    # Check board ownership
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this list"
        )

    list_obj = list_crud.update(db, db_obj=list_obj, obj_in=list_in)
    return list_obj


@router.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    *,
    db: Session = Depends(get_db),
    list_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete list (and all its cards via cascade).

    Args:
        db: Database session
        list_id: List ID
        current_user: Current authenticated user

    Raises:
        HTTPException: If list not found or user doesn't own parent board
    """
    list_obj = list_crud.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

    # Check board ownership
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this list"
        )

    list_crud.remove(db, id=list_id)


@router.patch("/lists/{list_id}/reorder", response_model=ListResponse)
def reorder_list(
    *,
    db: Session = Depends(get_db),
    list_id: UUID,
    reorder_data: ListReorder,
    current_user: User = Depends(get_current_active_user)
) -> List:
    """
    Change list position.

    Args:
        db: Database session
        list_id: List ID
        reorder_data: New position data
        current_user: Current authenticated user

    Returns:
        Updated list

    Raises:
        HTTPException: If list not found or user doesn't own parent board
    """
    list_obj = list_crud.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

    # Check board ownership
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reorder this list"
        )

    list_obj = list_crud.reorder(db, db_obj=list_obj, new_position=reorder_data.position)
    return list_obj
