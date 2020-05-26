from typing import Callable


class Broker:
    """
    The broker service.
    For simplicity, each broker instance supports one topic only.
    """

    def __init__(self, connector):
        self.connector = connector

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.connector.close()

    def publish(self, msg: str) -> None:
        """
        Publish data to the topic
        """
        self.connector.publish(msg)

    def subscribe_and_consume(self, consumer: Callable) -> None:
        """
        Subscribe to the topic
        The callback will be called upon each msg received
        """
        self.connector.subscribe(consumer)
        self.connector.consume()
