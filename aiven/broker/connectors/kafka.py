import logging

from kafka.errors import KafkaTimeoutError
from kafka import KafkaProducer, KafkaConsumer

from aiven.broker.connectors.api import BrokerConnector, PublishError
# or, if it were implemented as a protocol:
# from aiven.broker.connectors.api import BrokerConnector, PublishError, implements


log = logging.getLogger()

# the nicer/modern way (see ap.py) would be
# @implements(BrokerConnector)
# class Kafka:
class Kafka(BrokerConnector):
    """
    The Kafka concrete implementation of a broker connector
    """

    def __init__(self,
            uri: str,
            topic: str = '',
            producer: bool = False
        ):
        """
        uri: where to connect, i.e. where the broker service is
        topic: the topic queue, one only for now
        """
        self.url = uri
        self.topic = topic
        self.producer = producer and KafkaProducer(bootstrap_servers=[uri])
    
    def publish(self, msg: str):
        if self.producer:
            try:
                self.producer.send(self.topic, value=msg)
                log.info(msg)
            except KafkaTimeoutError as err:
                raise PublishError(err)
        else:
            raise PublishError("A consumer doesnt publish with this implementation")

    def subscribe(self, callback):
        self.callback = callback
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[self.uri]
        )

    def consume(self):
        for msg in self.consumer:
            self.callback(msg.value)
