import logging
import sys


class Log:
    def __init__(
        self,
        log_level: str,
        log_format: str,
        date_fmt: str,
    ) -> None:
        self.log_level = log_level
        self.log_format = log_format
        self.date_fmt = date_fmt

    def set_log_level(self) -> None:
        logging.basicConfig(
            stream=sys.stdout,
            format=self.log_format,
            level=self.log_level,
            datefmt=self.date_fmt,
        )
