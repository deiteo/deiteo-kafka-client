import asyncio
import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.deiteo_kafka.producer.deiteo_kafka_aio_producer import DeiteoKafkaAioProducer

TEST_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

FAKE_TOPIC = "deiteo-fake-input"
FAKE_BOOTSTRAP_SERVERS = "localhost-fake:1234"
DEITEO_KAFKA_AIO_PRODUCER_PATH = "src.deiteo_kafka.producer.deiteo_kafka_aio_producer"


@pytest.fixture(scope="function")
def mock_aio_kafka_producer() -> Generator[MagicMock, None, None]:
    with patch(f"{DEITEO_KAFKA_AIO_PRODUCER_PATH}.AIOKafkaProducer") as mocked_aio_kafka_producer:
        yield mocked_aio_kafka_producer

    mocked_aio_kafka_producer.reset_mock()


@pytest.fixture(scope="function")
def deiteo_kafka_aio_instance(
    event_loop, mock_aio_kafka_producer
) -> Generator[DeiteoKafkaAioProducer, None, None]:
    loop = asyncio.new_event_loop()

    yield DeiteoKafkaAioProducer(
        topic=FAKE_TOPIC, bootstrap_servers=FAKE_BOOTSTRAP_SERVERS, loop=loop
    )

    loop.close()
