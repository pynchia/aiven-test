import logging

import kafka
from kafka.errors import KafkaTimeoutError

from aiven.broker.connectors.api import BrokerConnector, PublishError
# or, if it were implemented as a protocol (see below and api.py):
# from aiven.broker.connectors.api import BrokerConnector, PublishError, implements


log = logging.getLogger()

# A nicer/more modern way (see api.py) could be:
# @implements(BrokerConnector)
# class Kafka:
class Kafka(BrokerConnector):
    """
    The Kafka concrete implementation of a broker connector
    """

    SSL_OPTIONS = {
        'security_protocol': 'SSL',
        'ssl_check_hostname': True,
        'ssl_cafile': '../kafka-pynchia/ca.pem',
        'ssl_certfile': '../kafka-pynchia/service.cert',
        'ssl_keyfile': '../kafka-pynchia/service.key'
    }


    def __init__(self,
            uri: str,
            topic: str = '',
            producer: bool = False
        ):
        """
        uri: where to connect, i.e. where the broker service is
        topic: the topic queue, one only for now
        """
        self.uri = uri
        self.topic = topic
        self.producer = producer and kafka.KafkaProducer(
            bootstrap_servers=uri,
            **self.SSL_OPTIONS
        )
    
    def publish(self, msg: str):
            try:
                self.producer.send(self.topic, value=msg.encode())
                log.info(msg)
            except KafkaTimeoutError as err:
                raise PublishError(err)
            except AttributeError:
                raise PublishError("A consumer cannot publish with this implementation")

    def subscribe(self, callback):
        self.callback = callback
        self.consumer = kafka.KafkaConsumer(
            self.topic,
            bootstrap_servers=self.uri,
            **self.SSL_OPTIONS
        )

    def consume(self):
        for msg in self.consumer:
            msg_str = msg.value.decode()
            log.info(msg_str)
            self.callback(msg_str)

    def close(self):
        pass
