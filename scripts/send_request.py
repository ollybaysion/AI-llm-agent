from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from uuid import uuid4

from confluent_kafka import Producer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
REQ_TOPIC = os.getenv("LLM_REQ_TOPIC", "llm.request")

def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def main() -> None:
    producer = Producer({"bootstrap.servers": BOOTSTRAP})

    job_id = f"job-{uuid4()}"
    user_id = os.getenv("USER_ID", "u-123")

    payload = {
        "jobId": job_id,
        "userId": user_id,
        "requestedAt": now_utc_iso(),
        "query": "강남에서 저녁 데이트 코스 추천해줘",
        "attributes": {
            "budget": 60000,
            "mood": "calm",
            "transport": "subway",
        },
    }

    gmsg = {
        "gId": str(uuid4()),
        "gDestination": "llm.request",
        "key": job_id,
        "createdAt": now_utc_iso(),
        "headers": {
            "contentType": "application/json",
            "x-request-type": "RECOMMEND",
        },
        "payload": payload,
    }

    producer.produce(
        REQ_TOPIC,
        key=job_id.encode("utf-8"),
        value=json.dumps(gmsg, ensure_ascii=False).encode("utf-8"),
    )
    producer.flush(5)

    print(f"sent to {REQ_TOPIC}: jobId={job_id}")

if __name__ == "__main__":
    main()
