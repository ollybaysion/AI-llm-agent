from app.agent import agent_call

def test_agent_call_basic():
    req = {
        "jobId": "job-1",
        "query": "강남 데이트",
        "attributes": {},
    }

    res = agent_call(req)
    assert res is not None