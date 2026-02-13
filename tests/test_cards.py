"""
Tests for card endpoints.
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


@pytest.fixture
def test_list(authenticated_client: TestClient, test_board: dict):
    """Create a test list."""
    response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "Test List", "position": 0}
    )
    return response.json()


def test_create_card(authenticated_client: TestClient, test_list: dict):
    """Test creating a card."""
    response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={
            "title": "Test Task",
            "description": "A test task",
            "position": 0,
            "priority": "high"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test task"
    assert data["position"] == 0
    assert data["priority"] == "high"
    assert data["list_id"] == test_list["id"]


def test_get_card(authenticated_client: TestClient, test_list: dict):
    """Test getting a card."""
    # Create card
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={"title": "Test Card", "position": 0}
    )
    card_id = create_response.json()["id"]

    # Get card
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/cards/{card_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Card"


def test_update_card(authenticated_client: TestClient, test_list: dict):
    """Test updating a card."""
    # Create card
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={"title": "Original Title", "position": 0}
    )
    card_id = create_response.json()["id"]

    # Update card
    response = authenticated_client.put(
        f"{settings.API_V1_PREFIX}/cards/{card_id}",
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "priority": "medium"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["priority"] == "medium"


def test_delete_card(authenticated_client: TestClient, test_list: dict):
    """Test deleting a card."""
    # Create card
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={"title": "Card to Delete", "position": 0}
    )
    card_id = create_response.json()["id"]

    # Delete card
    response = authenticated_client.delete(
        f"{settings.API_V1_PREFIX}/cards/{card_id}"
    )
    assert response.status_code == 204


def test_reorder_card(authenticated_client: TestClient, test_list: dict):
    """Test reordering a card."""
    # Create card
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={"title": "Test Card", "position": 0}
    )
    card_id = create_response.json()["id"]

    # Reorder card
    response = authenticated_client.patch(
        f"{settings.API_V1_PREFIX}/cards/{card_id}/reorder",
        json={"position": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == 3


def test_move_card(authenticated_client: TestClient, test_board: dict, test_list: dict):
    """Test moving a card to another list."""
    # Create second list
    list2_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/boards/{test_board['id']}/lists/",
        json={"title": "Second List", "position": 1}
    )
    list2_id = list2_response.json()["id"]

    # Create card in first list
    create_response = authenticated_client.post(
        f"{settings.API_V1_PREFIX}/lists/{test_list['id']}/cards/",
        json={"title": "Card to Move", "position": 0}
    )
    card_id = create_response.json()["id"]

    # Move card to second list
    response = authenticated_client.patch(
        f"{settings.API_V1_PREFIX}/cards/{card_id}/move",
        json={
            "list_id": list2_id,
            "position": 0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["list_id"] == list2_id
    assert data["position"] == 0


def test_card_not_found(authenticated_client: TestClient):
    """Test getting non-existent card."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = authenticated_client.get(
        f"{settings.API_V1_PREFIX}/cards/{fake_uuid}"
    )
    assert response.status_code == 404
