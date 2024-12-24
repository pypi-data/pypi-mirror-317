# Standard Library Imports
import asyncio
import time

# Local Imports
from .periodic_observer import PeriodicObserver
from ..bots import Bot


class TimeOutObserver(PeriodicObserver):
    """An `Observer` that stops the `Bot` from being run after a specified
    amount of time.

    This `Observer` periodically checks how long a `Bot` has been running for
    already. If this time exceeds some specified threshold the `Runner` will
    be stopped from running the `Bot`.
    """

    def __init__(self, bot: Bot, timeout: float, delay: float = .2) -> None:
        """Initializes the observer given a bot and delay.

        Args:
            bot (Bot): The bot to be observed.
            timeout (float): The time (in seconds) after which the bot will be stopped from being run.
            delay (float, optional): The delay (in seconds) between each observation cycle (default is 0.2).
        """
        super().__init__(bot, delay)
        self.timeout = timeout
        self.end_time: float | None = None

    async def _loop_function(self, stop_event: asyncio.Event) -> None:
        """Stops the bot from being run if the timeout was exceeded.

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        if self.end_time is None:
            self.end_time = time.time() + self.timeout
        if time.time() > self.end_time:
            stop_event.set()
