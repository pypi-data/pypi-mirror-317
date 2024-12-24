# Local Imports
from .solver import Solver
from ..utils.question_outcome import QuestionOutcome


class QuitSolver(Solver):
    """A `Solver` that always chooses to quit."""

    def solve(self, game_variables: dict) -> tuple[str, QuestionOutcome]:
        """Chooses to quit the question.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.

        Returns:
            tuple[str, QuestionOutcome]: A tuple of 'q' and the 'Incorrect' outcome.
        """
        return "q", QuestionOutcome(False, False)
