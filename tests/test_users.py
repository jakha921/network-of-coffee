import pytest
from fastapi import status

def test_register_user(client):
    response = client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "password" not in data

def test_register_user_duplicate_email(client):
    # Сначала регистрируем пользователя
    client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    
    # Пытаемся зарегистрировать пользователя с тем же email
    response = client.post(
        "/api/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST 