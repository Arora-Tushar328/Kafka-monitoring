import json
import logging
import os
import time

import requests
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("weather-producer")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("TOPIC", "weather-data")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "London", "lat": 51.5072, "lon": -0.1276},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
]


def fetch_weather(city):
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }
    response = requests.get(API_URL, params=params, timeout=15)
    response.raise_for_status()

    data = response.json().get("current", {})
    if not data:
        return None

    return {
        "city": city["name"],
        "temperature_c": data.get("temperature_2m", 0),
        "humidity": data.get("relative_humidity_2m", 0),
        "wind_speed": data.get("wind_speed_10m", 0),
        "timestamp": time.time(),
    }


while True:
    for city in CITIES:
        try:
            payload = fetch_weather(city)
            if payload:
                producer.send(TOPIC, payload)
                logger.info("Sent to %s: %s", TOPIC, payload)
            else:
                logger.warning("No weather data for %s", city["name"])
        except Exception as exc:
            logger.error("Error fetching/sending %s: %s", city["name"], exc)

        time.sleep(2)

    time.sleep(10)

