import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
LLM_REQ_TOPIC = os.getenv("LLM_REQ_TOPIC", "llm.request")
LLM_RES_TOPIC = os.getenv("LLM_RES_TOPIC", "llm.response")
LLM_GROUP_ID = os.getenv("LLM_GROUP_ID", "dataguide-llm-agent-v1")

