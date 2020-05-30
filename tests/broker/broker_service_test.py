"""
Test the Broker service
"""
import pytest
from unittest.mock import MagicMock, patch
from aiven.broker.connectors.kafka import Kafka
from aiven.broker.services.broker import Broker


def test_service_publish(sample_msg_str):
    message_queue = []  # the queue of messages, stored elsewhere
    def publish(msg):
        message_queue.append(msg)

    mock_kafka = MagicMock()
    with Broker(mock_kafka) as broker:
        assert broker.connector == mock_kafka

        mock_kafka.publish.side_effect = publish
        broker.publish(sample_msg_str)
        mock_kafka.publish.assert_called_once()
        assert message_queue.pop() == sample_msg_str
    mock_kafka.close.assert_called_once()


def test_service_subscribe_and_consume(sample_msg_str):
    consumer = lambda msg: None  # what to call back, stored in the connector
    message_queue = []  # the queue of messages, stored elsewhere

    def processor(msg):  # the actual callback, the end-user processing the msg
        assert msg == sample_msg_str
    def publish(msg):
        message_queue.append(msg)
    def subscribe(callback):
        nonlocal consumer
        consumer = callback
    def consume():
        msg = message_queue.pop(0)  # pop the oldest one in the queue
        consumer(msg)

    mock_kafka = MagicMock()
    with Broker(mock_kafka) as broker:
        assert broker.connector == mock_kafka

        mock_kafka.publish.side_effect = publish
        broker.publish(sample_msg_str)
        mock_kafka.publish.assert_called_once()
    mock_kafka.close.assert_called_once()

    mock_kafka = MagicMock() # another broker for another consumer process
    with Broker(mock_kafka) as broker:
        assert broker.connector == mock_kafka

        mock_kafka.publish.side_effect = publish
        broker.publish(sample_msg_str)
        mock_kafka.publish.assert_called_once()

        mock_kafka.subscribe.side_effect = subscribe
        mock_kafka.consume.side_effect = consume
        broker.subscribe_and_consume(processor)
        mock_kafka.subscribe.assert_called_once()
        mock_kafka.consume.assert_called_once()
    mock_kafka.close.assert_called_once()
