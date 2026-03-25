from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True
    secret_token: str

class ItemResponse(BaseModel):
    name: str
    price: float
    is_available: bool


# 임시 데이터
fake_db = {
    1: {"name": "커피", "price": 4500.0, "is_available": True},
    2: {"name": "녹차", "price": 3000.0, "is_available": False}
}

def common_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@router.get("")
def read_items(commons: dict = Depends(common_params)):
    return {"params": commons}

@router.get("/{item_id}")
def read_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을수 없습니다")
    return fake_db[item_id]

@router.post("", response_model=ItemResponse)
def create_item(item: ItemCreate):
    if item.price <= 0 :
        raise HTTPException(status_code=404, detail="가격은 0보다 커야 합니다")
    return item

