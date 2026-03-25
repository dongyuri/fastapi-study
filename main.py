
from fastapi import FastAPI, Depends
from routers import items


app = FastAPI(
    title = "FastAPI 학습 프로젝트",
    description = "dongyuri의 FastAPI 학습 기록",
    version = "0.1.0"
)

app.include_router(items.router)


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI!"}



