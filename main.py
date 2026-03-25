
from fastapi import FastAPI
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

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI!"}

# Path Parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# POST 요청
@app.post("/items", response_model=ItemResponse, tags=["items"])
def create_item(item: ItemCreate):
    return item

