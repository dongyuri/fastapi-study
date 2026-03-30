from fastapi.testclient import TestClient
from main import app
from app.database import get_connection
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    yield

# 회원가입
def test_register():
    response = client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "dongyuri"

# 중복 회원가입
def test_register_duplicate():
    client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    response = client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    assert response.status_code == 400

# 로그인
def test_login():
    client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    response = client.post("/users/login",
        data={"username": "dongyuri", "password": "1234"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# 잘못된 비밀번호 로그인
def test_login_wrong_password():
    client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    response = client.post("/users/login",
        data={"username": "dongyuri", "password": "wrong"}
    )
    assert response.status_code == 401

# 내 정보 조회
def test_read_me():
    client.post("/users/register", json={
        "username": "dongyuri",
        "password": "1234"
    })
    login = client.post("/users/login",
        data={"username": "dongyuri", "password": "1234"}
    )
    token = login.json()["access_token"]

    response = client.get("/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "dongyuri"

# 토큰 없이 내 정보 조회
def test_read_me_without_token():
    response = client.get("/users/me")
    assert response.status_code == 401
