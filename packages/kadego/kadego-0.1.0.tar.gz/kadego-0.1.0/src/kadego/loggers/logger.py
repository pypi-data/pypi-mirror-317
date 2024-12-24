# Standard Library Imports
from abc import ABC, abstractmethod


class Logger(ABC):
    """An Abstract base class for logging game variables.

    A `Logger` is used by a `Bot` to log game data. Each time the solution
    to a question is revealed the `Bot` will call the `Logger` to log the
    current game variables.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Initializes the logger."""
        pass

    @abstractmethod
    def log(self, game_variables: dict) -> None:
        """Logs the given game variables.

        Args:
            game_variables (dict): The game variables shortly after a solution was revealed.
        """
        pass
