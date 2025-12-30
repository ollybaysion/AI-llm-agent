from confluent_kafka import Consumer
from .config import KAFKA_BOOTSTRAP, LLM_GROUP_ID, LLM_REQ_TOPIC

def build_consumer() -> Consumer:
    c = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": LLM_GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    })
    c.subscribe([LLM_REQ_TOPIC])
    return c