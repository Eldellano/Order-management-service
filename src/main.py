import uvicorn
from fastapi import FastAPI

from api.routers.main_router import main_router
from settings import settings

app = FastAPI(
    title="Order management service",
    description="Пример сервиса управления заказами",
    version="0.1",
)


app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port)
