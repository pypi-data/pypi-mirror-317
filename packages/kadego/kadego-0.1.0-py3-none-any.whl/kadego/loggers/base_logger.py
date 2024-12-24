# Local Imports
from .logger import Logger


class BaseLogger(Logger):
    """A basic `Logger` that does not do actual logging"""

    def __init__(self) -> None:
        """Initializes the logger."""
        return

    def log(self, game_variables: dict) -> None:
        """Does not do anything.

        Args:
            game_variables (dict): The game variables shortly after a solution was revealed.
        """
        return
