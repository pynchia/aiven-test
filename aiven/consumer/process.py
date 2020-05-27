"""
The functionality to process the incoming metrics
"""

from datetime import datetime
import json
import logging

import psycopg2 as pg

from aiven.broker.services.message import Message


log = logging.getLogger()


class MessageDecodeError(Exception):
    pass


class Processor:
    """
    Process the incoming messages from the broker.
    It stores the messages in the PostgreSQL db (such functionality is now hard-wired here
     but it should be decoupled)
    """

    def __init__(self, db_uri):
        # self.db = pg.connect(db_uri, )
        pass

    def __call__(self, msg: str):
        """
        Process the incoming msg from the meter
        """
        log.info(f"Received msg {msg}")
        try:
            message = Message.parse(msg)
        except MessageDecodeError as e:
            log.error(e)
        else:
            # add to DB
            log.info(f"Msg {msg} saved to DB")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        # close DB cnx
        pass
