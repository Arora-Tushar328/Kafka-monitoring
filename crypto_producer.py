import json
import logging
import os
import time
import requests
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("crypto-producer")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("TOPIC", "crypto-data")
URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

while True:
    try:
        data = requests.get(URL, timeout=10).json()
        payload = {
            "bitcoin_usd": data.get("bitcoin", {}).get("usd", 0),
            "ethereum_usd": data.get("ethereum", {}).get("usd", 0),
            "timestamp": time.time(),
        }
        producer.send(TOPIC, payload)
        logger.info("Sent: %s", payload)
    except Exception as e:
        logger.error("Error: %s", e)
    time.sleep(10)

