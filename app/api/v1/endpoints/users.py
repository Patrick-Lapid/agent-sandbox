from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.crud.user import user as user_crud
from app.schemas.user import UserUpdate, UserResponse, UserUpdatePassword
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()


@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Update current user profile.

    Args:
        db: Database session
        user_in: User update data
        current_user: Current authenticated user

    Returns:
        Updated user

    Raises:
        HTTPException: If email or username already exists
    """
    # Check if email is being updated and already exists
    if user_in.email and user_in.email != current_user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    # Check if username is being updated and already exists
    if user_in.username and user_in.username != current_user.username:
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Update user
    user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.patch("/me/password", response_model=UserResponse)
def update_password_me(
    *,
    db: Session = Depends(get_db),
    password_in: UserUpdatePassword,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Update current user password.

    Args:
        db: Database session
        password_in: Password update data
        current_user: Current authenticated user

    Returns:
        Updated user

    Raises:
        HTTPException: If current password is incorrect
    """
    # Verify current password
    if not verify_password(password_in.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    # Update password
    user = user_crud.update_password(
        db, user=current_user, new_password=password_in.new_password
    )
    return user
