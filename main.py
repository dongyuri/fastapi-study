
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI(
    title = "FastAPI 학습 프로젝트",
    description = "dongyuri의 FastAPI 학습 기록",
    version = "0.1.0"
)

# 입력 스키마
class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True
    secret_token: str

# 응답 스키마
class ItemResponse(BaseModel):
    name: str
    price: float
    is_available: bool

# 공통 쿼리 파라미터 의존성
def common_params(skip: int=0, limit: int=10):
    return {"skip": skip, "limit": limit}

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/items", tags=["items"])
def read_items(commons: dict = Depends(common_params)):
    return {"params": commons}

@app.get("/users", tags=["users"])
def read_users(commons: dict = Depends(common_params)):
    return {"params": commons}

@app.post("/items", response_model=ItemResponse, tags=["items"])
def create_item(item: ItemCreate):
    return item

