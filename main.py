
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import items, users
from app.database import init_db
import logging


# 로깅 설정 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("서버 시작 및 DB 초기화 완료")
    yield


app = FastAPI(
    title = "FastAPI 학습 프로젝트",
    description = "dongyuri의 FastAPI 학습 기록",
    version = "0.1.0",
    lifespan=lifespan
)


# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router)
app.include_router(users.router)


@app.get("/", tags=["root"])
def read_root():
    logger.info("루트 엔드포인트 호출됨")
    return {"message": "Hello, FastAPI!"}



