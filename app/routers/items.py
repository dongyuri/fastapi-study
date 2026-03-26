
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool

# CREATE
@router.post("", response_model=ItemResponse)
def create_item(item: ItemCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items (name, price, is_available)
        VALUES (?, ?, ?)
        """, (item.name, item.price, item.is_available))

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return {**item.dict(), "id": item_id}

# READ ALL
@router.get("", response_model=list[ItemResponse])
def read_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()

    return [dict(item) for item in items]

# READ ONE
@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    return dict(item)

# UPDATE
@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    cursor.execute("""
        UPDATE items
        SET name = ?, price = ?, is_available = ?
        WHERE id = ?
    """, (item.name, item.price, item.is_available, item_id))

    conn.commit()
    conn.close()

    return {**item.dict(), "id": item_id}

# DELETE
@router.delete("/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return {"message": "아이템이 삭제되었습니다"}


