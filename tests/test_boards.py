"""
Tests for board endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


def test_create_board(authenticated_client: TestClient):
    """Test creating a board."""
    response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={
            "title": "My First Board",
            "description": "A test board"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Board"
    assert data["description"] == "A test board"
    assert "id" in data
    assert "owner_id" in data


def test_list_boards(authenticated_client: TestClient):
    """Test listing boards."""
    # Create two boards
    authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Board 1"}
    )
    authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Board 2"}
    )

    # List boards
    response = authenticated_client.get(f"{settings.API_V1_PREFIX}/boards/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Board 1"
    assert data[1]["title"] == "Board 2"


def test_get_board(authenticated_client: TestClient):
    """Test getting a board."""
    # Create board
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Test Board"}
    )
    board_id = create_response.json()["id"]

    # Get board
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/boards/{board_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Board"
    assert "lists" in data


def test_get_board_not_found(authenticated_client: TestClient):
    """Test getting non-existent board."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/boards/{fake_uuid}"
    )
    assert response.status_code == 404


def test_update_board(authenticated_client: TestClient):
    """Test updating a board."""
    # Create board
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Original Title"}
    )
    board_id = create_response.json()["id"]

    # Update board
    response = authenticated_client.put(
        f"{settings.API_V1_PREFIX}/boards/{board_id}",
        json={
            "title": "Updated Title",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"


def test_delete_board(authenticated_client: TestClient):
    """Test deleting a board."""
    # Create board
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Board to Delete"}
    )
    board_id = create_response.json()["id"]

    # Delete board
    response = authenticated_client.delete(
        f"{settings.API_V1_PREFIX}/boards/{board_id}"
    )
    assert response.status_code == 204

    # Verify deletion
    get_response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/boards/{board_id}"
    )
    assert get_response.status_code == 404


def test_create_board_unauthorized(client: TestClient):
    """Test creating board without authentication."""
    response = client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Unauthorized Board"}
    )
    assert response.status_code == 401
