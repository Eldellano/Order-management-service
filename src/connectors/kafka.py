import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from settings import settings

kafka_host = settings.kafka_host
kafka_port = settings.kafka_port
kafka_topic = settings.kafka_topic

kafka_server = f"{kafka_host}:{kafka_port}"


async def send_kafka_message(key: str, message: dict):
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_server,
        key_serializer=lambda k: json.dumps(key, default=str).encode("utf-8")
        if k is not None
        else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
    )

    await producer.start()
    try:
        await producer.send_and_wait(kafka_topic, key=key, value=message)
    finally:
        await producer.stop()


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
                case _:
                    print(f"Received message: {message.key=}, {message.value=}")

    finally:
        await consumer.stop()

