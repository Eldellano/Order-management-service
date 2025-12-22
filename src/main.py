import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from api.routers.main_router import main_router
from connectors.kafka import kafka_consumer_loop, start_producer, stop_producer
from connectors.redis_db import redis_db
from settings import settings

consumer_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_task

    await FastAPILimiter.init(redis_db)

    await start_producer()

    consumer_task = asyncio.create_task(kafka_consumer_loop())

    yield
    await FastAPILimiter.close()

    await stop_producer()

    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Order management service",
    description="Пример сервиса управления заказами",
    version="0.1",
    lifespan=lifespan,
)


origins = [
    "http://localhost:3000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port)
