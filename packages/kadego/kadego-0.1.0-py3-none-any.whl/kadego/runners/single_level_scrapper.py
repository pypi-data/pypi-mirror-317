# Third-Party Imports
from playwright.async_api import Page

# Local Imports
from .runner import Runner
from ..bots.bot import Bot
from ..loggers.single_level_words_logger import SingleLevelWordsLogger
from ..observers.progress_bar_observer import ProgressBarObserver
from ..strategies.curious_strategy import CuriousStrategy


class SingleLevelScraper(Runner):
    """A runner for scraping the word data of individual levels from 漢字でGO!.

    This class sets up a `Bot` configured to play the 'Rush' mode with the
    `CuriousStrategy` as well as a `SingleLevelWordsLogger` to log the
    scraped words and a `ProgressBarObserver` to display the progress.
    """
    def __init__(self, kadego: Page, level: int, path: str) -> None:
        """Initializes the runner with all its components.

        Args:
            kadego (Page): The Playwright page for playing 漢字でGO!.
            level (int): The level to be scraped for words.
            path (str): The file path where the scraped data will be stored.
        """
        logger = SingleLevelWordsLogger(level, path)
        strategy = CuriousStrategy()

        bot = Bot(kadego, "rush", f"level_{level}", strategy, logger=logger)
        observer = ProgressBarObserver(bot)

        super().__init__(bot, observer)
