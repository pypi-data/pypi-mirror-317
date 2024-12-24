# Standard Library Imports
import asyncio

# Third-Party Imports
from tqdm import tqdm

# Local Imports
from .periodic_observer import PeriodicObserver
from ..bots import Bot
from ..exceptions import IncompatibleBotError
from ..loggers import SingleLevelWordsLogger


class ProgressBarObserver(PeriodicObserver):
    """An `Observer` priting the current status of a `Bot` as well as the
    progress via a progress bar.

    This `Observer` is meant to work together with a `Bot` that has an
    instance of `SingleLevelWordsLogger` as its `Logger`. A progress bar
    is printed that shows how many distinct words' data was already
    collected and updates periodically. Once all words' data hase been
    collected the `Runner` will be stopped from running the `Bot`.
    """

    def __init__(self, bot: Bot, delay: float = .2) -> None:
        """Initializes the observer given a bot and delay.

        Args:
            bot (Bot): The bot to be observed.
            delay (float, optional): The delay (in seconds) between each observation cycle (default is 0.2).
        """
        super().__init__(bot, delay)
        if not isinstance(bot.logger, SingleLevelWordsLogger):
            raise IncompatibleBotError("The logger of the bot must be an instance of 'SingleLevelWordsLogger'.")
        assert isinstance(self.bot.logger, SingleLevelWordsLogger)
        self.progress_bar: tqdm = tqdm(total=len(self.bot.logger.data))

    def _loop_function(self, stop_event: asyncio.Event) -> None:
        """Updates the progress bar based on the bot's logger data and stops
        the `Runner` from running the `Bot` once all words' data has been
        collected.

        Args:
            stop_event (asyncio.Event): Event that when set stops the runner from running the bot.
        """
        assert isinstance(self.bot.logger, SingleLevelWordsLogger)
        non_nones = sum(1 for value in self.bot.logger.data.values() if value is not None)

        self.progress_bar.set_description(self.bot.status[:50].ljust(50))
        self.progress_bar.n = non_nones
        self.progress_bar.refresh()

        if non_nones == self.progress_bar.total:
            stop_event.set()
            self.progress_bar.close()
