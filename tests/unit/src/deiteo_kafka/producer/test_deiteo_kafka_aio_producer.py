from unittest.mock import call

import pytest
from freezegun import freeze_time

from tests.conftest import FAKE_TOPIC

FREEZE_TIME = "2022-03-26T15:00:00"


@pytest.mark.usefixtures("deiteo_kafka_aio_instance")
@freeze_time(FREEZE_TIME)
@pytest.mark.parametrize(
    "topic_content, expected_produced_data",
    [({"A": 0}, b"{'A': 0, 'ingestion_utc_ts': '2022-03-26T15:00:00'}")],
)
@pytest.mark.asyncio
async def test_produce(deiteo_kafka_aio_instance, topic_content, expected_produced_data) -> None:
    await deiteo_kafka_aio_instance.produce(topic_content=topic_content)
    assert deiteo_kafka_aio_instance.producer.send_and_wait.call_args_list == [
        call(FAKE_TOPIC, expected_produced_data)
    ]
