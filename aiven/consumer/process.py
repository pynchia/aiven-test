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
     but we may want to decouple it)
    """

    def __init__(self, db_uri):
        self.db_connection = pg.connect(
            db_uri,
            # sslmode='verify-full',
            sslrootcert='../pg-pynchia/ca.pem'
        )
        self.db_connection.autocommit = True

    def __call__(self, msg: str):
        """
        Process the incoming msg
        """
        print('\n***************** Processor called with', msg)
        log.info(f"Received msg {msg}")
        try:
            message = Message.parse(msg)
        except MessageDecodeError as e:
            log.error(e)
        else:
            # add to DB
            with self.db_connection.cursor() as cursor:
                try:
                    cursor.execute("""
                        INSERT INTO metrics
                        (timestamp, elapsed, status, pattern_ack)
                        values (%s, %s, %s, %s);""",
                        (message.timestamp, message.elapsed, message.status, message.pattern_ack)
                    )
                except (pg.Error, AttributeError) as err:
                    log.error(err)
                else:
                    log.info(f"Msg {msg} saved to DB")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        # close DB cnx
        self.db_connection.close()
