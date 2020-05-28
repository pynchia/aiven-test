from datetime import datetime
import json
import pytest
from aiven.broker.services.message import Message


@pytest.fixture(scope='session')
def sample_msg_dict_bad_keys():
    return {
        "timestamp": "2020-05-27 11:42:01",
        "xyz": 1234
    }

@pytest.fixture(scope='session')
def sample_msg_str_bad_keys(sample_msg_dict_bad_keys):
    return json.dumps(sample_msg_dict_bad_keys)
