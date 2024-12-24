# Standard Library Imports
from abc import ABC, abstractmethod

# Local Imports
from ..utils.question_outcome import QuestionOutcome


class Solver(ABC):
    """ An abstract base class for solving a question.

    A `Solver` chooses an answer and a corresponding `QuestionOutcome`
    given the game variables.
    """

    def __init__(self) -> None:
        """Initializes the solver."""
        return

    @abstractmethod
    def solve(self, game_variables: dict) -> tuple[str, QuestionOutcome]:
        """Chooses an answer and an outcome based on provided game variables.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.

        Returns:
            tuple[str, QuestionOutcome]: A tuple of the chosen answer and the corresponding outcome.
        """
        pass
