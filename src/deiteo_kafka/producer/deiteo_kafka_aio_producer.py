import logging
from asyncio import AbstractEventLoop, get_event_loop
from datetime import datetime
from typing import Any, Dict, Optional, Union

from aiokafka import AIOKafkaProducer
from aiokafka.errors import (
    BrokerResponseError,
    KafkaConnectionError,
    MessageSizeTooLargeError,
    ProducerClosed,
    UnsupportedVersionError,
)
from deiteo_kafka.log import Log


class DeiteoKafkaAioProducer:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        log_level: str = "INFO",
        log_format: str = "%(asctime)s %(levelname)-8s %(message)s",
        date_fmt: str = "%Y-%m-%d %H:%M:%S",
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        Log(
            log_format=log_format,
            date_fmt=date_fmt,
            log_level=log_level,
        ).set_log_level()

        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.loop = loop if loop else self._get_running_loop()
        self.producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
        )

    @staticmethod
    def _get_running_loop() -> AbstractEventLoop:
        loop = get_event_loop()

        if not loop.is_running():
            err_msg = "The loop should be created within an async function or provide directly"
            raise RuntimeError(err_msg)

        return loop

    @staticmethod
    def _add_ingestion_ts(topic_content: Dict[str, Any]) -> None:
        topic_content["ingestion_utc_ts"] = datetime.utcnow().isoformat()

    async def _send_and_wait(self, topic_content: Union[str, Dict[str, Any]]) -> None:
        try:
            logging.debug(f"Call aio-kafka produce send and wait %s", topic_content)

            if isinstance(topic_content, dict):
                self._add_ingestion_ts(topic_content=topic_content)

            elif isinstance(topic_content, str):
                topic_content = {"data": topic_content}
                self._add_ingestion_ts(topic_content=topic_content)

            await self.producer.send_and_wait(
                self.topic,
                bytes(str(topic_content), "utf-8"),
            )
            logging.debug(f"Successfully produced to topic %s", self.topic)

        except (
            BrokerResponseError,
            KafkaConnectionError,
            MessageSizeTooLargeError,
            ProducerClosed,
            UnsupportedVersionError,
        ) as produce_error:
            logging.error(f"Produce Error: %s", produce_error)

    async def produce(
        self,
        topic_content: Union[str, Dict[str, Any]],
    ) -> None:
        await self._send_and_wait(topic_content=topic_content)
