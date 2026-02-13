"""
Script to create initial superuser from environment variables.

Run this script after database migrations to create the first superuser account.

Usage:
    python -m app.initial_data
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate
from app.models.user import User


def init_db(db: Session) -> None:
    """
    Initialize database with first superuser.

    Args:
        db: Database session
    """
    # Check if superuser already exists
    user = user_crud.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="System Administrator"
        )
        user = user_crud.create(db, obj_in=user_in)

        # Set as superuser
        user.is_superuser = True
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"✓ Superuser created: {user.email}")
    else:
        print(f"✓ Superuser already exists: {user.email}")


def main() -> None:
    """Main function to initialize database."""
    print("Creating initial data...")
    db = SessionLocal()
    try:
        init_db(db)
        print("✓ Initial data created successfully!")
    except Exception as e:
        print(f"✗ Error creating initial data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
