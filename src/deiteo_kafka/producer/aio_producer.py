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
from deiteo_kafka.log import Log
from deiteo_kafka.utils import DeiteoUtils


class AioProducerError(
    MessageSizeTooLargeError,
    UnsupportedVersionError,
    BrokerResponseError,
    KafkaConnectionError,
    ProducerClosed,
    RuntimeError,
):
    pass


class AioProducer:
    def __init__(
        self,
        topic: str,
        bootstrap_servers: str,
        debug_mode: bool = False,
        log_level: str = "INFO",
        log_format: str = "%(asctime)s %(levelname)-8s %(message)s",
        date_fmt: str = "%Y-%m-%d %H:%M:%S",
        loop: Optional[AbstractEventLoop] = None,
        utils: Optional[DeiteoUtils] = None,
    ) -> None:
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.debug_mode = debug_mode
        self.log_level = log_level
        self.log_format = log_format
        self.date_fmt = date_fmt
        self.utils = DeiteoUtils() if not utils else utils

        if not loop and self.utils:
            self.loop = self.utils.get_running_loop()
        else:
            self.loop = loop

        self.producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.bootstrap_servers,
        )

    def _setup_log(self) -> None:
        log = Log(
            log_format=self.log_format,
            date_fmt=self.date_fmt,
            log_level=self.log_level,
        )
        log.set_log_level()

    async def _stop_producer(self) -> None:
        try:
            await self.producer.stop()

        except RuntimeError as run_time_error:
            raise run_time_error

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

        except AioProducerError as aio_producer_error:
            logging.error(f"Something went wrong! {aio_producer_error}")

    async def stop_producer(self, stop_loop: bool = False) -> None:
        try:
            await self._stop_producer()

            if stop_loop:
                self.loop.stop()

        except AioProducerError as aio_producer_error:
            raise aio_producer_error
