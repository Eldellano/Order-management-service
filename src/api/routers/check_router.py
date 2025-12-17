from fastapi import APIRouter

from api.schemas import GenericErrorResponse, GenericResponse

health_check_router = APIRouter(tags=["health_check_api"])


@health_check_router.get(
    "/health",
    description="Проверка состояния запуска сервиса",
    responses={
        200: {"model": GenericResponse},
        400: {"model": GenericErrorResponse},
        404: {"model": GenericErrorResponse},
    },
)
async def health_check():
    """Эндпоинт для проверки состояния сервиса внутри docker compose health check"""

    return GenericResponse(message="ok")
