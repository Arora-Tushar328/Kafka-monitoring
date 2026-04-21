import json
import logging
import os
import time
import requests
import xml.etree.ElementTree as ET
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("news-producer")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("TOPIC", "news-data")
RSS_URL = "https://feeds.bbci.co.uk/news/world/rss.xml"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

while True:
    try:
        xml_data = requests.get(RSS_URL, timeout=10).text
        root = ET.fromstring(xml_data)
        item = root.find("./channel/item")
        payload = {
            "headline": item.findtext("title", default=""),
            "link": item.findtext("link", default=""),
            "timestamp": time.time(),
        }
        producer.send(TOPIC, payload)
        logger.info("Sent: %s", payload)
    except Exception as e:
        logger.error("Error: %s", e)
    time.sleep(20)

