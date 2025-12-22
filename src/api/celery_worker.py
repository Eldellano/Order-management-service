import time
from connectors.celery_conf import celery_app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task(name="tasks.process_order")
def process_order(order_id: str):
    time.sleep(2)
    logger.info(f"Order {order_id} processed")
    print(f"Order {order_id} processed")