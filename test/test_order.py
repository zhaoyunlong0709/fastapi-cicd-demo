from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "user_id": 1001,
            "start": "北京南站",
            "end": "望京",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1001
    assert data["status"] == "CREATED"


def test_get_not_exist_order():
    response = client.get("/orders/999999")
    assert response.status_code == 404


def test_cancel_order():
    create_response = client.post(
        "/orders",
        json={
            "user_id": 1002,
            "start": "西二旗",
            "end": "中关村",
        },
    )

    order_id = create_response.json()["id"]

    cancel_response = client.post(f"/orders/{order_id}/cancel")

    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "CANCELED"
