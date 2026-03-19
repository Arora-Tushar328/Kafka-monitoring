import os
import time
import json
import logging
import requests
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = "weather-data"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
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
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        current = payload.get("current", {})
        if not current:
            logging.warning("Empty current weather for %s: %s", city["name"], payload)
            return None

        return {
            "city": city["name"],
            "temperature_c": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "timestamp": time.time()
        }
    except Exception as e:
        logging.error("Open-Meteo error for %s: %s", city["name"], e)
        return None

while True:
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            producer.send(TOPIC, data)
            logging.info("Sent: %s", data)
        time.sleep(2)
    time.sleep(30)

