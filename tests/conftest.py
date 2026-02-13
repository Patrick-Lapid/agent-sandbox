"""
Pytest configuration and fixtures for tests.
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate
from app.core.security import create_access_token

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a fresh database for each test.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db) -> Generator:
    """
    Create a test client with database override.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db) -> dict:
    """
    Create a test user.
    """
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpassword123",
        full_name="Test User"
    )
    user = user_crud.create(db, obj_in=user_in)
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "password": "testpassword123",  # Plain password for login tests
        "user": user
    }


@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, test_user: dict) -> TestClient:
    """
    Create an authenticated test client.
    """
    # Login to get access token
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Set authorization header
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture(scope="function")
def test_user_token(test_user: dict) -> str:
    """
    Create an access token for test user.
    """
    return create_access_token(subject=str(test_user["id"]))
