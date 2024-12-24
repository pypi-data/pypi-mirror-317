# Local Imports
from .solver import Solver
from ..utils.question_outcome import QuestionOutcome


class SkipSolver(Solver):
    """A `Solver` that always chooses to skip."""

    def solve(self, game_variables: dict) -> tuple[str, QuestionOutcome]:
        """Chooses to skip the question.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.

        Returns:
            tuple[str, QuestionOutcome]: A tuple of an empty string and the 'Skipped' outcome.
        """
        return "", QuestionOutcome(True, True)
