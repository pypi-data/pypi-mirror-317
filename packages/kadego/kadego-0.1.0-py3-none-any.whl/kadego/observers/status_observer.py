# Standard Library Imports
import asyncio

# Local Imports
from .periodic_observer import PeriodicObserver


class StatusObserver(PeriodicObserver):
    """An `Observer` priting the current status of a `Bot`.

    This `Observer` prints the current state of a `Bot` periodically
    overwriting it.
    """

    def _loop_function(self, stop_event: asyncio.Event) -> None:
        """Prints the current state of the bot.

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        status = self.bot.status
        print(f"\rStatus: {status}\033[K", end='', flush=True)
