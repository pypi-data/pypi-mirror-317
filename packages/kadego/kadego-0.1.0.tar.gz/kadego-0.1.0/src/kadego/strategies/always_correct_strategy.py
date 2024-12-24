# Local Imports
from .strategy import Strategy
from ..solvers.correct_solver import CorrectSolver
from ..solvers.solver import Solver
from ..utils.game_status import GameStatus


class AlwaysCorrectStrategy(Strategy):
    """A `Strategy` that always chooses the `CorrectSolver` to answer
    questions."""

    def get_solver(self, game_variables: dict, status: GameStatus) -> Solver:
        """Chooses the correct answer to the question.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.
            status (GameStatus): The current game status (e.g. number of lives)

        Returns:
            tuple[str, QuestionOutcome]: A tuple of the correct answer and the 'Correct' outcome.
        """
        return CorrectSolver()
