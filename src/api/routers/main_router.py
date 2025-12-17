from fastapi import APIRouter

from api.routers.check_router import health_check_router
from api.routers.order_router import order_router
from api.routers.user_router import user_router

main_router = APIRouter(prefix="/api")

main_router.include_router(health_check_router)
# main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(order_router)