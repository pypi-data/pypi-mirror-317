# Standard Library Imports
import asyncio
from abc import ABC, abstractmethod

# Local Imports
from ..bots.bot import Bot


class Observer(ABC):
    """An Abstract base class for observing a bot.

    An `Observer` runs in parallel to a `Bot` reacting to changes in its
    state or outside factors e.g. by stopping the `Runner` from running
    the `Bot`.
    """

    def __init__(self, bot: Bot):
        """Initializes the observer given a bot.

        Args:
            bot (Bot): The bot to be observed.
        """
        self.bot: Bot = bot

    @abstractmethod
    async def observe(self, stop_event: asyncio.Event) -> None:
        """Observes the bot reacting to changes or outside factors.

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        pass
