from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from confluent_kafka import KafkaException
from pydantic import ValidationError

from dotenv import load_dotenv

from .consumer import build_consumer
from .producer import build_producer
from .config import LLM_RES_TOPIC
from .agent import agent_call

from .model.gmessage import GMessage
from .model.recommend import RecommendLlmRequest, RecommendLlmResponse

load_dotenv()

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def main() -> None:
    consumer = build_consumer()
    producer = build_producer()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            try:
                raw = json.loads(msg.value().decode("utf-8"))
                greq = GMessage[RecommendLlmRequest].model_validate(raw)
            except (json.JSONDecodeError, ValidationError) as e:
                print("[INVALID_MESSAGE]", e)
                consumer.commit(message=msg, asynchronous=False)
                continue

            req = greq.payload
            out = agent_call(req.model_dump())

            inner = RecommendLlmResponse(
                jobId=req.jobId,
                messageId=str(uuid4()),
                createdAt=now_utc(),
                payload=out,
            )

            out_key = greq.key or req.jobId
            gres = GMessage[RecommendLlmResponse](
                gId=str(uuid4()),
                gDestination="llm.response",
                key=out_key,
                createdAt=now_utc(),
                headers=greq.headers,
                payload=inner,
            )

            producer.produce(
                LLM_RES_TOPIC,
                key=out_key.encode("utf-8"),
                value=gres.model_dump_json().encode("utf-8"),
            )
            producer.flush(5)

            consumer.commit(message=msg, asynchronous=False)

    finally:
        consumer.close()

if __name__ == "__main__":
    main()