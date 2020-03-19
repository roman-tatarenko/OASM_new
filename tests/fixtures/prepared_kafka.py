from json import dumps

import pytest
from kafka import KafkaProducer, KafkaConsumer


@pytest.fixture(scope='function')
def producer(kafka_bootstrap_servers):
    return KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


@pytest.fixture(scope='function')
def consumer(kafka_bootstrap_servers):
    return KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=None,
        max_poll_records=5,
        consumer_timeout_ms=180000)
