
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.database import get_connection
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

# 현재 로그인한 유저 가져오기
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (payload.get("sub"),))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise HTTPException(status_code=401, detail="유저를 찾을 수 없습니다")
    return dict(user)

# 회원가입
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="이미 존재하는 유저입니다")

    hashed = hash_password(user.password)
    cursor.execute("""
        INSERT INTO users (username, hashed_password)
        VALUES (?, ?)
    """, (user.username, hashed))

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return {"id": user_id, "username": user.username}

# 로그인
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    user = cursor.fetchone()
    conn.close()

    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# 내 정보 조회
@router.get("/me", response_model=UserResponse)
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
