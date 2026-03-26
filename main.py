
from fastapi import FastAPI
from app.routers import items
from app.database import init_db


app = FastAPI(
    title = "FastAPI 학습 프로젝트",
    description = "dongyuri의 FastAPI 학습 기록",
    version = "0.1.0"
)

app.include_router(items.router)

@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI!"}



