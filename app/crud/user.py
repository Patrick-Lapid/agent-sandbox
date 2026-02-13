from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model."""

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            db: Database session
            email: User email

        Returns:
            User instance if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: Username

        Returns:
            User instance if found, None otherwise
        """
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create new user with hashed password.

        Args:
            db: Database session
            obj_in: User creation schema

        Returns:
            Created user instance
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_superuser=False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user by email and password.

        Args:
            db: Database session
            email: User email
            password: Plain text password

        Returns:
            User instance if authentication succeeds, None otherwise
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """Check if user is superuser."""
        return user.is_superuser

    def update_password(
        self, db: Session, *, user: User, new_password: str
    ) -> User:
        """
        Update user password.

        Args:
            db: Database session
            user: User instance
            new_password: New plain text password

        Returns:
            Updated user instance
        """
        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser(User)
