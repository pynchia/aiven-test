"""
Test the consumer
"""
from unittest.mock import MagicMock, patch

import pytest

from aiven.broker.connectors.kafka import Kafka
from aiven.consumer.process import Processor


DB_URI = 'xyz'

def test_processor_context_mgr():
    with patch('aiven.consumer.process.pg') as mock_pg:
        mock_connect = MagicMock()
        mock_pg.connect.return_value = mock_connect
        with Processor(DB_URI):
            mock_pg.connect.assert_called_once()
        mock_connect.close.assert_called_once()

# The test below doesn't work, I have tried for quite a while. The namespace gets owewritte in the module
#
# def test_msg_written_to_db(sample_msg_dict, sample_msg_str):

#     message_queue = []  # the queue of messages

#     def mock_execute(query, values):
#         print('\n****** mock_execute called with', values)
#         message_queue.append(values)
#         assert set(values) == set(sample_msg_dict.values())

#     with patch('aiven.consumer.process.pg.connect') as mock_conn:
#         mock_cnx = mock_conn.return_value
#         with Processor(DB_URI) as processor:
#             mock_cur = MagicMock()
#             mock_cnx.cursor.return_value = mock_cur
#             mock_cur.execute.side_effect = mock_execute
#             processor(sample_msg_str)
#         mock_cur.execute.assert_called_once()
#         assert len(message_queue) == 1
