import json
import logging
import os
from kafka import KafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("weather-consumer")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("TOPIC", "weather-data")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "weather-consumer-group")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=CONSUMER_GROUP,
    auto_offset_reset="latest",
    enable_auto_commit=True,
)

logger.info(
    "Starting consumer | broker=%s topic=%s group=%s",
    KAFKA_BROKER,
    TOPIC,
    CONSUMER_GROUP,
)

for message in consumer:
    try:
        payload = json.loads(message.value.decode("utf-8"))
        logger.info("Received | topic=%s group=%s payload=%s", TOPIC, CONSUMER_GROUP, payload)
    except json.JSONDecodeError:
        logger.warning("Skipping non-JSON message: %s", message.value)
    except Exception as exc:
        logger.error("Consumer error: %s", exc)

