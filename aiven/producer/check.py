from datetime import datetime
from time import sleep

# from aiven.broker.services.message import Message


def generate_metrics(website: str, freq: int):
    """
    Generate the metrics by checking the website is up
    Params:
        freq - Frequency in seconds between checks
        website - the uri of the website to check
    Yields: the generated metrics
    """

    def poll():
        """
        Poll the website to see if it's available
        """
        return 200

    while True:
        # data = poll()
        timestamp = datetime.now()
        # message = Message(
        #     timestamp=timestamp,
        #     status=data
        # )
        # yield str(message)
        yield str(timestamp)
        sleep(freq) # wait for a while
