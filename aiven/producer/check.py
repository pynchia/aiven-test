from datetime import datetime
import re
from time import sleep

import requests

from aiven.broker.services.message import Message


TIMEOUT = 5  # max number of seconds to wait for a response


def generate_metrics(website: str, delay: int, pattern: str):
    """
    Generate the metrics by checking the website is up
    Params:
        website - the uri of the website to check
        freq - Frequency in seconds between checks
        pattern - the pattern to search in the response (regex string)
    Yields: the metrics message
    """

    def is_pattern_present(content):
        return bool(pattern_compiled.search(content))

    def poll_website():
        """
        Poll the website to monitor its availability
        """
        response = requests.get(website, timeout=TIMEOUT)
        return (
            response.elapsed.total_seconds(),
            response.status_code,
            is_pattern_present(response.text)
        )

    pattern_compiled = re.compile(pattern)
    while True:
        timestamp = datetime.now()
        elapsed, status, pattern_ack = poll_website()
        message = Message(
            timestamp=timestamp,
            elapsed=elapsed,
            status=status,
            pattern_ack=pattern_ack
        )
        yield str(message)
        sleep(delay) # wait for a while
