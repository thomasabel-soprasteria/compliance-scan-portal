
import pytest
from httpx import AsyncClient
import json

@pytest.mark.asyncio
async def test_create_requirement(client: AsyncClient):
    """Test creating a new regulatory requirement."""
    response = await client.post(
        "/api/v1/requirements/",
        json={
            "name": "Test Requirement",
            "description": "This is a test requirement",
            "category": "Test",
            "active": True
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Requirement"
    assert data["description"] == "This is a test requirement"
    assert data["category"] == "Test"
    assert data["active"] == True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

@pytest.mark.asyncio
async def test_get_requirements(client: AsyncClient):
    """Test listing regulatory requirements."""
    # First create a requirement
    await client.post(
        "/api/v1/requirements/",
        json={
            "name": "Test Requirement",
            "description": "This is a test requirement",
            "category": "Test",
            "active": True
        }
    )
    
    # Get all requirements
    response = await client.get("/api/v1/requirements/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == "Test Requirement"

@pytest.mark.asyncio
async def test_get_requirement_by_id(client: AsyncClient):
    """Test getting a specific requirement by ID."""
    # First create a requirement
    create_response = await client.post(
        "/api/v1/requirements/",
        json={
            "name": "Test Requirement",
            "description": "This is a test requirement",
            "category": "Test",
            "active": True
        }
    )
    
    requirement_id = create_response.json()["id"]
    
    # Get the requirement by ID
    response = await client.get(f"/api/v1/requirements/{requirement_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == requirement_id
    assert data["name"] == "Test Requirement"

@pytest.mark.asyncio
async def test_update_requirement(client: AsyncClient):
    """Test updating a regulatory requirement."""
    # First create a requirement
    create_response = await client.post(
        "/api/v1/requirements/",
        json={
            "name": "Test Requirement",
            "description": "This is a test requirement",
            "category": "Test",
            "active": True
        }
    )
    
    requirement_id = create_response.json()["id"]
    
    # Update the requirement
    response = await client.patch(
        f"/api/v1/requirements/{requirement_id}",
        json={
            "name": "Updated Requirement",
            "active": False
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == requirement_id
    assert data["name"] == "Updated Requirement"
    assert data["description"] == "This is a test requirement"  # Unchanged
    assert data["active"] == False  # Changed

@pytest.mark.asyncio
async def test_delete_requirement(client: AsyncClient):
    """Test deleting a regulatory requirement."""
    # First create a requirement
    create_response = await client.post(
        "/api/v1/requirements/",
        json={
            "name": "Test Requirement",
            "description": "This is a test requirement",
            "category": "Test",
            "active": True
        }
    )
    
    requirement_id = create_response.json()["id"]
    
    # Delete the requirement
    response = await client.delete(f"/api/v1/requirements/{requirement_id}")
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = await client.get(f"/api/v1/requirements/{requirement_id}")
    assert get_response.status_code == 404
