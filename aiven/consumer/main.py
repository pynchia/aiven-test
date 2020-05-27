"""
The main module of the Consumer application
"""

from aiven.broker.connectors.kafka import Kafka
from aiven.broker.services.broker import Broker
from aiven.consumer.process import Processor


def main(kafka_uri: str, topic: str, db_uri: str):
    kafka_client = Kafka(kafka_uri, topic)
    with Broker(kafka_client) as broker, Processor(db_uri) as processor:
        broker.subscribe_and_consume(consumer=processor)
