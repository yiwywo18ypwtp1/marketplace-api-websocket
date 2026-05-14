import pytest


@pytest.mark.asyncio
async def test_create_order_unauthorized(client):
    response = await client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": 1,
        },
    )

    assert response.status_code == 401