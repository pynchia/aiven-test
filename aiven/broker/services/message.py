from datetime import datetime
import json
from typing import NamedTuple


TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class MessageFormatError(Exception):
    pass


class Message(NamedTuple):
    timestamp: str  # when the msg was created
    elapsed: float  # how long it took to respond (s)
    status: int  # HTTP response status code
    pattern_ack: bool  # if the pattern was found on the page

    @classmethod
    def parse(cls, msg: str):
        """
        Parse the incoming string msg into a structured message
        Return:
            the message
        """
        try:
            msg_d = json.loads(msg)
            message = cls(**msg_d)
        except (json.JSONDecodeError, TypeError, ValueError):
            raise MessageFormatError(f"Malformed message received: {msg}")
        return message

    def __str__(self):
        """
        The msg serialised as json:
            '{
                "timestamp": timestamp (in the above string format),
                "elapsed": 123,
                "status": 200;
                "pattern_ack": true
            }'
        """
        msg_d = self._asdict()
        msg_d['timestamp'] = datetime.strftime(self.timestamp, TIMESTAMP_FORMAT)
        return json.dumps(msg_d)
