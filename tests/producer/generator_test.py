from datetime import datetime
import itertools as it
import random
from unittest.mock import MagicMock, patch

import requests
import pytest

from aiven.broker.services.message import Message
from aiven.producer.generate import generate_metrics, TIMESTAMP_FORMAT


def test_format_of_generated_msgs():
    """
    Test the generator produces good messages
    """

    PATTERN = 'coordination'
    DELAY = 0.3
    ELAPSED = 0.42
    STATUS = 200
    TEXT = """
        <!doctype html>
        <html>
        <head>
            <title>Example Domain</title>
            <meta charset="utf-8" />
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
        <div>
            <h1>Example Domain</h1>
            <p>This domain is for use in illustrative examples in documents. You may use this
            domain in literature without prior coordination or asking for permission.</p>
            <p><a href="https://www.iana.org/domains/example">More information...</a></p>
        </div>
        </body>
        </html>
        """

    def mock_http_get(uri, **kwargs):
        response = MagicMock()
        response.elapsed.total_seconds.return_value = ELAPSED
        response.status_code = STATUS
        response.text = TEXT
        return response

    with patch('aiven.producer.generate.requests.get', side_effect=mock_http_get):
        for msg in it.islice(
                    generate_metrics(
                        'xyz',
                        DELAY,
                        PATTERN
                    ),
                    0, 3):  # retrieve a few messages
            msg = Message.parse(msg)  # check the message is valid
            assert type(msg.timestamp) is str
            datetime.strptime(msg.timestamp, TIMESTAMP_FORMAT)  # check it is a valid timestamp
            assert msg.elapsed == ELAPSED
            assert msg.status == STATUS
            assert msg.pattern_ack
