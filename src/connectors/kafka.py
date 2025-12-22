import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from api.celery_worker import process_order
from settings import settings

kafka_host = settings.kafka_host
kafka_port = settings.kafka_port
kafka_topic = settings.kafka_topic

kafka_server = f"{kafka_host}:{kafka_port}"

producer: AIOKafkaProducer | None = None  # глобальный продюсер kafka


async def start_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=kafka_server,
            key_serializer=lambda k: json.dumps(k, default=str).encode("utf-8")
            if k is not None
            else None,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        )
        await producer.start()


async def stop_producer():
    global producer
    if producer is not None:
        await producer.stop()
        producer = None


async def send_kafka_message(key: str, message: dict):
    if producer is None:
        await start_producer()
    await producer.send_and_wait(kafka_topic, key=key, value=message)


async def kafka_consumer_loop():
    consumer = AIOKafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_server,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for message in consumer:
            key = None
            if message.key is not None:
                key_str = message.key.decode("utf-8")  # bytes в строку
                try:
                    key = json.loads(key_str)  # если ключ был сериализован через JSON
                except json.JSONDecodeError:
                    key = key_str

            match key:
                case "new_order":
                    print("Receive new order")
                    order_data = message.value
                    order_id = order_data.get("id")

                    process_order.delay(order_id)

                case _:
                    print(f"Received message: {message.key=}, {message.value=}")

    finally:
        await consumer.stop()

