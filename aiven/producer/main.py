"""
The main module of the producer application
"""

import logging
from aiven.producer.check import generate_metrics
from aiven.broker.connectors.kafka import Kafka
from aiven.broker.services.broker import Broker


log = logging.getLogger()


def main(kafka_uri: str, topic: str, web_uri: str, delay: int, pattern: str):
    kafka_client = Kafka(kafka_uri, topic, producer=True)
    with Broker(kafka_client) as broker:
        for msg in generate_metrics(web_uri, delay, pattern):
            broker.publish(msg)
