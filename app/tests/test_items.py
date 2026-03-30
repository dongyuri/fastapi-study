

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# GET / 테스트
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}


# GET /items 테스트
def test_read_items():
    response = client.get("/items")
    assert response.status_code == 200


# GET /items/{item_id} 정상 조회
def test_read_item_success():
    # 먼저 아이템 생성 후 id 가져오기
    create = client.post("/items", json={"name": "커피", "price": 4500.0})
    item_id = create.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "커피"


# GET /items/{item_id} 존재하지 않는 아이템
def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "아이템을 찾을 수 없습니다"


# POST /items 정상 생성
def test_create_item_success():
    response = client.post("/items", json={
        "name": "아메리카노",
        "price": 4000.0,
        "is_available": True,
        "secret_token": "abc1234"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "아메리카노"
    assert "secret_token" not in response.json()


# POST /items 가격 오류
def test_create_item_invalid_price():
    response = client.post("/items", json={
        "name": "아메리카노",
        "price": -1000.0,
        "is_available": True,
        "secret_token": "abc1234"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "가격은 0보다 커야 합니다"


