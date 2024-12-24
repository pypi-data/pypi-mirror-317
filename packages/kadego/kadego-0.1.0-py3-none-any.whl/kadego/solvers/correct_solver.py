# Local Imports
from .solver import Solver
from ..utils.question_outcome import QuestionOutcome


class CorrectSolver(Solver):
    """A `Solver` that always chooses the correct answer."""

    def solve(self, game_variables: dict) -> tuple[str, QuestionOutcome]:
        """Chooses the correct answer to the question.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.

        Returns:
            tuple[str, QuestionOutcome]: A tuple of the correct answer and the 'Correct' outcome.
        """
        return game_variables["_data"][9], QuestionOutcome(True, False)
