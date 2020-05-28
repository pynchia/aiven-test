from datetime import  datetime
import json
import pytest


@pytest.fixture(scope='session')
def sample_msg_dict():
    return {
        "timestamp": "2020-05-27 11:42:01",
        "elapsed": 0.42,
        "status": 200,
        "pattern_ack": True
    }

@pytest.fixture(scope='session')
def sample_msg_str(sample_msg_dict):
    return json.dumps(sample_msg_dict)
