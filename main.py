
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Path Parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Query Parameter
@app.get("/search")
def search_item(q: str, limit: int=10):
    return {"query": q, "limit": limit}

# Pydantic 모델정의
class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True

# POST 요청
@app.post("/items")
def create_item(item: Item):
    return {"message": "아이템 생성완료", "item": item}
