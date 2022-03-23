import asyncio
import logging
from asyncio import AbstractEventLoop
from datetime import datetime
from typing import Any, Dict, Optional

from aiokafka import AIOKafkaProducer
from aiokafka.errors import (
    BrokerResponseError,
    KafkaConnectionError,
    MessageSizeTooLargeError,
    ProducerClosed,
    UnsupportedVersionError,
)
from log import Log


class KafkaClientError(
    MessageSizeTooLargeError,
    UnsupportedVersionError,
    BrokerResponseError,
    KafkaConnectionError,
    ProducerClosed,
):
    pass


class Client:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        debug_mode: bool = False,
        log_level: str = "INFO",
        log_format: str = "%(asctime)s %(levelname)-8s %(message)s",
        date_fmt: str = "%Y-%m-%d %H:%M:%S",
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        log = Log(log_format=log_format, date_fmt=date_fmt, log_level=log_level)
        log.set_log_level()
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.debug_mode = debug_mode
        self.log_level = log_level
        self.loop = asyncio.get_event_loop() if not loop else loop
        self.producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
        )

    async def _send_and_wait(self, topic_content: Dict[str, Dict[str, Any]]) -> None:
        try:
            logging.debug(
                f"Call aio-kafka produce send and wait: {topic_content} \n"
                f"and wait, ts: {datetime.utcnow()}\n"
                f"Topic Content: {topic_content}"
            )

            if not self.debug_mode:
                await self.producer.send_and_wait(
                    self.topic,
                    bytes(str(topic_content), "utf-8"),
                )

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
        topic_content: Dict[str, Dict[str, Any]],
    ) -> None:
        try:
            await self.producer.start()
            await self._send_and_wait(topic_content=topic_content)

        except KafkaClientError as kafka_client_error:
            logging.error(f"Something went wrong! {kafka_client_error}")
