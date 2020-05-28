"""
Test the Kafka connector
"""

from typing import NamedTuple
from unittest.mock import MagicMock, patch

from kafka.errors import KafkaTimeoutError
import pytest

from aiven.broker.connectors.api import PublishError
from aiven.broker.connectors.kafka import Kafka


def test_connector_publish(sample_msg_str):
    message_queue = []  # the queue of messages

    def send(topic, value):
        message_queue.append(value)

    with patch('aiven.broker.connectors.kafka.kafka') as mock_kafka:
        kafka_producer = MagicMock()
        mock_kafka.KafkaProducer.return_value = kafka_producer
        connector = Kafka('broker_uri', 'topic', producer=True)
        kafka_producer.send.side_effect = send
        connector.publish(sample_msg_str)
        assert len(message_queue) == 1
        assert message_queue[0] == sample_msg_str.encode()

def test_connector_publish_fail_timeout(sample_msg_str):
    TEST_ERROR = 'test_error'

    def send(topic, value):
        raise KafkaTimeoutError(TEST_ERROR)

    with patch('aiven.broker.connectors.kafka.kafka') as mock_kafka:
        kafka_producer = MagicMock()
        mock_kafka.KafkaProducer.return_value = kafka_producer
        connector = Kafka('broker_uri', 'topic', producer=True)
        kafka_producer.send.side_effect = send
        with pytest.raises(PublishError) as err:
            connector.publish(sample_msg_str)
        assert str(err.value).endswith(TEST_ERROR)


class KafkaMessage(NamedTuple):
    """
    The message, as stored by Kafka
    """
    value: bytes


def test_connector_subscribe_and_consume(sample_msg_str):
    message_queue = []  # the queue of messages

    def send(topic, value):
        message_queue.append(KafkaMessage(value))

    def processor(msg):  # the callback, the end-user processing the msg
        assert msg == sample_msg_str
        message_queue.pop()

    with patch('aiven.broker.connectors.kafka.kafka') as mock_kafka:
        kafka_producer = MagicMock()
        mock_kafka.KafkaProducer.return_value = kafka_producer
        connector = Kafka('broker_uri', 'topic', producer=True)
        kafka_producer.send.side_effect = send
        connector.publish(sample_msg_str)
        assert len(message_queue) == 1
        assert message_queue[0].value == sample_msg_str.encode()

        mock_kafka.KafkaConsumer.return_value = message_queue
        connector.subscribe(processor)
        assert connector.callback is processor
        assert connector.consumer is message_queue
        
        connector.consume()
        assert len(message_queue) == 0  # the message was consumed
