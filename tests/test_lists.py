"""
Tests for list endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


@pytest.fixture
def test_board(authenticated_client: TestClient):
    """Create a test board."""
    response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/",
        json={"title": "Test Board"}
    )
    return response.json()


def test_create_list(authenticated_client: TestClient, test_board: dict):
    """Test creating a list."""
    response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={
            "title": "To Do",
            "position": 0
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "To Do"
    assert data["position"] == 0
    assert data["board_id"] == test_board["id"]


def test_get_list(authenticated_client: TestClient, test_board: dict):
    """Test getting a list."""
    # Create list
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "Test List", "position": 0}
    )
    list_id = create_response.json()["id"]

    # Get list
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/lists/{list_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test List"


def test_update_list(authenticated_client: TestClient, test_board: dict):
    """Test updating a list."""
    # Create list
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "Original Title", "position": 0}
    )
    list_id = create_response.json()["id"]

    # Update list
    response = authenticated_client.put(
        f"{settings.API_V1_PREFIX}/lists/{list_id}",
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_list(authenticated_client: TestClient, test_board: dict):
    """Test deleting a list."""
    # Create list
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "List to Delete", "position": 0}
    )
    list_id = create_response.json()["id"]

    # Delete list
    response = authenticated_client.delete(
        f"{settings.API_V1_PREFIX}/lists/{list_id}"
    )
    assert response.status_code == 204


def test_reorder_list(authenticated_client: TestClient, test_board: dict):
    """Test reordering a list."""
    # Create list
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "Test List", "position": 0}
    )
    list_id = create_response.json()["id"]

    # Reorder list
    response = authenticated_client.patch(
        f"{settings.API_V1_PREFIX}/lists/{list_id}/reorder",
        json={"position": 5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == 5


def test_list_not_found(authenticated_client: TestClient):
    """Test getting non-existent list."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/lists/{fake_uuid}"
    )
    assert response.status_code == 404
