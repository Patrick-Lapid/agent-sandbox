from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.board import board as board_crud
from app.crud.list import list_crud
from app.crud.card import card as card_crud
from app.schemas.card import CardCreate, CardUpdate, CardResponse, CardMove, CardReorder
from app.models.user import User
from app.models.card import Card

router = APIRouter()


@router.post("/lists/{list_id}/cards/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(
    *,
    db: Session = Depends(get_db),
    list_id: UUID,
    card_in: CardCreate,
    current_user: User = Depends(get_current_active_user)
) -> Card:
    """
    Create a new card in a list.

    Args:
        db: Database session
        list_id: Parent list ID
        card_in: Card creation data
        current_user: Current authenticated user

    Returns:
        Created card

    Raises:
        HTTPException: If list not found or user doesn't own parent board
    """
    # Check if list exists and user owns parent board
    list_obj = list_crud.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this list"
        )

    # Create card
    card = card_crud.create_in_list(db, obj_in=card_in, list_id=list_id)
    return card


@router.get("/cards/{card_id}", response_model=CardResponse)
def get_card(
    *,
    db: Session = Depends(get_db),
    card_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> Card:
    """
    Get card by ID.

    Args:
        db: Database session
        card_id: Card ID
        current_user: Current authenticated user

    Returns:
        Card

    Raises:
        HTTPException: If card not found or user doesn't own parent board
    """
    card = card_crud.get(db, id=card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )

    # Check board ownership through list
    list_obj = list_crud.get(db, id=card.list_id)
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this card"
        )

    return card


@router.put("/cards/{card_id}", response_model=CardResponse)
def update_card(
    *,
    db: Session = Depends(get_db),
    card_id: UUID,
    card_in: CardUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Card:
    """
    Update card.

    Args:
        db: Database session
        card_id: Card ID
        card_in: Card update data
        current_user: Current authenticated user

    Returns:
        Updated card

    Raises:
        HTTPException: If card not found or user doesn't own parent board
    """
    card = card_crud.get(db, id=card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )

    # Check board ownership through list
    list_obj = list_crud.get(db, id=card.list_id)
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this card"
        )

    card = card_crud.update(db, db_obj=card, obj_in=card_in)
    return card


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    *,
    db: Session = Depends(get_db),
    card_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete card.

    Args:
        db: Database session
        card_id: Card ID
        current_user: Current authenticated user

    Raises:
        HTTPException: If card not found or user doesn't own parent board
    """
    card = card_crud.get(db, id=card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )

    # Check board ownership through list
    list_obj = list_crud.get(db, id=card.list_id)
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this card"
        )

    card_crud.remove(db, id=card_id)


@router.patch("/cards/{card_id}/move", response_model=CardResponse)
def move_card(
    *,
    db: Session = Depends(get_db),
    card_id: UUID,
    move_data: CardMove,
    current_user: User = Depends(get_current_active_user)
) -> Card:
    """
    Move card to a different list.

    Args:
        db: Database session
        card_id: Card ID
        move_data: Target list and position
        current_user: Current authenticated user

    Returns:
        Updated card

    Raises:
        HTTPException: If card or target list not found, or user doesn't own parent board
    """
    card = card_crud.get(db, id=card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )

    # Check current board ownership
    current_list = list_crud.get(db, id=card.list_id)
    current_board = board_crud.get(db, id=current_list.board_id)
    if current_board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to move this card"
        )

    # Check target list exists and belongs to same board
    target_list = list_crud.get(db, id=move_data.list_id)
    if not target_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target list not found"
        )

    if target_list.board_id != current_board.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot move card to a list in a different board"
        )

    # Move card
    card = card_crud.move_to_list(
        db, db_obj=card, list_id=move_data.list_id, position=move_data.position
    )
    return card


@router.patch("/cards/{card_id}/reorder", response_model=CardResponse)
def reorder_card(
    *,
    db: Session = Depends(get_db),
    card_id: UUID,
    reorder_data: CardReorder,
    current_user: User = Depends(get_current_active_user)
) -> Card:
    """
    Change card position within the same list.

    Args:
        db: Database session
        card_id: Card ID
        reorder_data: New position data
        current_user: Current authenticated user

    Returns:
        Updated card

    Raises:
        HTTPException: If card not found or user doesn't own parent board
    """
    card = card_crud.get(db, id=card_id)
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )

    # Check board ownership through list
    list_obj = list_crud.get(db, id=card.list_id)
    board = board_crud.get(db, id=list_obj.board_id)
    if board.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reorder this card"
        )

    card = card_crud.reorder(db, db_obj=card, new_position=reorder_data.position)
    return card
