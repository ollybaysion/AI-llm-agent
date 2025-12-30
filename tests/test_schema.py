from app.model.gmessage import GMessage
from app.model.recommend import RecommendLlmRequest
from pydantic import ValidationError

def test_recommend_request_valid():
    data = {
        "gId": "g1",
        "gDestination": "llm.request",
        "key": "job-1",
        "createdAt": "2025-12-30T10:00:00Z",
        "headers": {},
        "payload": {
            "jobId": "job-1",
            "userId": "u-1",
            "requestedAt": "2025-12-30T09:59:00Z",
            "query": "강남 데이트",
            "attributes": {"budget": 50000},
        },
    }

    msg = GMessage[RecommendLlmRequest].model_validate(data)
    assert msg.payload.jobId == "job-1"

def test_recommend_request_invalid_missing_field():
    data = {
        "gId": "g1",
        "gDestination": "llm.request",
        "key": "job-1",
        "createdAt": "2025-12-30T10:00:00Z",
        "headers": {},
        "payload": {
            # No JobId
            "userId": "u-1",
            "requestedAt": "2025-12-30T09:59:00Z",
            "query": "강남 데이트",
            "attributes": {"budget": 50000},
        },
    }

    try:
        GMessage[RecommendLlmRequest].model_validate(data)
        assert False, "ValidationError expected"
    except ValidationError:
        pass

