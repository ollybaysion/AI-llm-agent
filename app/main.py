import json
import time
from confluent_kafka import KafkaException

from .consumer import build_consumer
from .producer import build_producer
from .config import LLM_RES_TOPIC
from .agent import agent_call

def main():
    consumer = build_consumer()
    producer = build_producer()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            key = msg.key().decode("utf-8") if msg.key() else None
            req = json.loads(msg.value().decode("utf-8"))

            job_id = req.get("jobId")
            try:
                out = agent_call(req)
                res = {
                    "jobId": job_id,
                    "status": "SUCCESS",
                    "payload": out,
                    "error": None,
                    "createdAt": int(time.time() * 1000),
                }
            except Exception as e:
                res = {
                    "jobId": job_id,
                    "status": "FAIL",
                    "payload": None,
                    "error": {"message": str(e), "type": e.__class__.__name__},
                    "createdAt": int(time.time() * 1000),
                }

            producer.produce(
                LLM_RES_TOPIC,
                key=key.encode("utf-8") if key else None,
                value=json.dumps(res, ensure_ascii=False).encode("utf-8"),
            )
            producer.flush(5)

            consumer.commit(message=msg, asynchronous=False)

    finally:
        consumer.close()

if __name__ == "__main__":
    main()