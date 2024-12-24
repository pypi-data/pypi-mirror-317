# Standard Library Imports
import asyncio

# Local Imports
from ..bots.bot import Bot
from ..observers.observer import Observer


class Runner:
    """A class responsible for running a bot playing 漢字でGO!

    A `Runner` can launch a `Bot` and an `Observer` to monitor the bot's
    activity.
    """
    def __init__(self, bot: Bot, observer: Observer) -> None:
        """Initializes the runner with a bot and an optional observer.

        Args:
            bot (Bot): The bot that will be launched and executed by the Runner.
            observer (Observer): The observer for the bot.
        """
        self.bot: Bot = bot
        self.observer: Observer = observer
        self.stop_event: asyncio.Event = asyncio.Event()

    async def run(self) -> None:
        """Starts running the bot in a loop as well as the observer.

        This method launches the bot and starts monitoring the bot's
        activity. The bot will continue running in a loop until the
        observer sends a signal to stop.
        """
        asyncio.create_task(self.observer.observe(self.stop_event))
        await self.bot.launch()

        while not self.stop_event.is_set():
            await self.bot.run()
