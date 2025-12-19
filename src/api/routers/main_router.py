from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from api.routers.check_router import health_check_router
from api.routers.order_router import order_router
from api.routers.user_router import user_router

main_router = APIRouter(prefix="/api")

main_router.include_router(health_check_router, dependencies=[])

main_router.include_router(
    user_router, dependencies=[Depends(RateLimiter(times=5, seconds=60))]
)
main_router.include_router(
    order_router, dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)