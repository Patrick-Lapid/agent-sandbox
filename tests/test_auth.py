"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


def test_register_user(client: TestClient):
    """Test user registration."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client: TestClient, test_user: dict):
    """Test registration with duplicate email."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json={
            "email": test_user["email"],
            "username": "differentusername",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client: TestClient, test_user: dict):
    """Test registration with duplicate username."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/register",
        json={
            "email": "different@example.com",
            "username": test_user["username"],
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client: TestClient, test_user: dict):
    """Test successful login."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user: dict):
    """Test login with wrong password."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={
            "username": test_user["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401


def test_get_current_user(authenticated_client: TestClient, test_user: dict):
    """Test getting current user info."""
    response = authenticated_client.get(f"{settings.API_V1_PREFIX}/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]


def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without authentication."""
    response = client.get(f"{settings.API_V1_PREFIX}/auth/me")
    assert response.status_code == 401
