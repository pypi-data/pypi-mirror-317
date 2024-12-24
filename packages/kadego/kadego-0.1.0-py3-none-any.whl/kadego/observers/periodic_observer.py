# Standard Library Imports
import asyncio
from abc import abstractmethod

# Local Imports
from .observer import Observer
from ..bots import Bot


class PeriodicObserver(Observer):
    """An abstract base class where the observation is performed periodically.

    This `Observer` performs the observation in a loop periodically waiting
    for a specified amount of time.
    """

    def __init__(self, bot: Bot, delay: float = .2) -> None:
        """Initializes the observer given a bot and delay.

        Args:
            bot (Bot): The bot to be observed.
            delay (float, optional): The delay (in seconds) between each observation cycle (default is 0.2).
        """
        super().__init__(bot)
        self.delay: float = delay

    @abstractmethod
    def _loop_function(self, stop_event: asyncio.Event) -> None:
        """Performs the actual observation

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        pass

    async def observe(self, stop_event: asyncio.Event) -> None:
        """Runs the function performing the actual observation in a loop.

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        while not stop_event.is_set():
            self._loop_function(stop_event)
            await asyncio.sleep(self.delay)
