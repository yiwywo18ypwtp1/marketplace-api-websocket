import pytest


@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post(
        "/users/signup",
        json={
            "email": "test@example.com",
            "username": "test",
            "password": "1234567vocem",
            "role": "buyer",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["username"] == "test"


@pytest.mark.asyncio
async def test_login(client):
    response = await client.post(
        "/users/login",
        json={
            "email": "test@example.com",
            "password": "1234567vocem",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "token" in data