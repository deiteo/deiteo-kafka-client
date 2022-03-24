import logging
from asyncio import AbstractEventLoop, get_event_loop


class UtilsDeiteoException(RuntimeError):
    pass


class DeiteoUtils:
    def __init__(self) -> None:
        self.loop = self.get_running_loop()

    @staticmethod
    def _get_running_loop() -> AbstractEventLoop:
        loop = get_event_loop()

        if not loop.is_running():
            err_msg = "The loop should be created within an async function or provide directly"
            raise RuntimeError(err_msg)

        return loop

    def get_running_loop(self) -> AbstractEventLoop:
        try:
            return self._get_running_loop()

        except UtilsDeiteoException as utils_deiteo_exception:
            logging.error(f"UtilsDeiteoException: %s", utils_deiteo_exception)
            raise utils_deiteo_exception
