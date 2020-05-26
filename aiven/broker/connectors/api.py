"""
API of the broker connector
it describes the operations allowed
independent of kind (e.g. Kafka, RabbitMQ, MQTT, etc)
"""

from abc import ABC, abstractmethod
from typing import Callable


class PublishError(Exception):
    pass


class BrokerConnector(ABC):
    """
    Basic interface to a broker every connector must implement
    """

    @abstractmethod
    def publish(self, msg: str) -> None:
        """
        Publish msg to the topic/queue
        """
        ...

    @abstractmethod
    def subscribe(self, callback: Callable) -> None:
        """
        Subscribe to the topic/queue passed to constructor
        callback: the worker to which each incoming msg must be passed
        """
        ...

    @abstractmethod
    def consume(self) -> None:
        """
        Consume msgs from the queue, endlessly
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Close the connection if needed, tidy up
        """
        ...


# Another way, maybe nicer/more modern way would be:
#
# from typing import Protocol, ContextManager, runtime_checkable
#
#
# @runtime_checkable
# class BrokerConnector(Protocol, ContextManager):
#     """
#     Basic interface to a broker.
#     Each broker instance support one queue only
#
#     Instantiate with params
#     url: URI of kafka broker
#     topic: name of topic
#     """
#     def publish(self, msg: str) -> None:
#         """
#         Publish message to the topic/queue
#         """
#         ...
#
#     def subscribe(self, callback: Callable) -> None:
#         """
#         Subscribe to the topic/queue passed to constructor
#         """
#         ...
#
#     def consume(self) -> None:
#         """
#         Consume messages from the topic/queue, endlessly
#         """
#         ...
#
#     def close(self) -> None:
#         """
#         Close the connection if needed, tidy up
#         """
#         ...
#
#
# def implements(proto: Type):
#     """ Creates a decorator for classes that checks that the decorated class
#     implements the runtime protocol `proto`
#     """
#     def _deco(cls_def):
#         try:
#             assert issubclass(cls_def, proto)
#         except AssertionError as e:
#             e.args = (f"{cls_def} does not implement protocol {proto}",)
#             raise
#         return cls_def
#     return _deco
