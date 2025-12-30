from confluent_kafka import Producer
from .config import KAFKA_BOOTSTRAP

def build_producer() -> Producer:
    return Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})