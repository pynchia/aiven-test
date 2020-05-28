from datetime import datetime
import json
from typing import NamedTuple


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
            raise MessageFormatError(f"Malformed message: {msg}")

        # Validate the type of field values
        # unfortunately NamedTuple doesn't allow subclasses to override __init__
        for attr, val in msg_d.items():
           if type(val) is not message._field_types[attr]:
                raise MessageFormatError(
                    f"Malformed message: {msg}\n"
                    f"Type of field {attr} is {type(val)} instead of {message._field_types[attr]} "
                )
        return message

    def __str__(self):
        """
        The msg serialised as json:
            '{
                "timestamp": timestamp string,
                "elapsed": 123,
                "status": 200;
                "pattern_ack": true
            }'
        """
        return json.dumps(self._asdict())
