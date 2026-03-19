import json
import os
import logging
from kafka import KafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "weather-data"

def safe_json(value: bytes):
    try:
        return json.loads(value.decode("utf-8"))
    except Exception:
        return None

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    value_deserializer=safe_json,
    group_id="weather-consumer-group"
)

logging.info("Starting weather consumer...")
for message in consumer:
    if message.value is None:
        logging.warning("Skipped non-JSON message at offset %s", message.offset)
        continue
    logging.info("Received: %s", message.value)

