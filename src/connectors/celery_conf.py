from celery import Celery
from settings import settings

redis_host = settings.redis_host
redis_port = settings.redis_port
redis_user = settings.redis_user
redis_pass = settings.redis_pass

celery_app = Celery(
    "worker",
    broker=f"redis://{redis_user}:{redis_pass}@{redis_host}:{redis_port}/0",
)

celery_app.conf.task_routes = {
    "tasks.process_order": {"queue": "orders"}
}
