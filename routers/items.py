from fastapi import APIRouter, Depends
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

def common_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@router.get("")
def read_items(commons: dict = Depends(common_params)):
    return {"params": commons}

@router.post("", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return item
