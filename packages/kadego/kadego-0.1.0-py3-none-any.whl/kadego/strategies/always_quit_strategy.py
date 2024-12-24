# Local Imports
from .strategy import Strategy
from ..solvers.quit_solver import QuitSolver
from ..solvers.solver import Solver
from ..utils.game_status import GameStatus


class AlwaysQuitStrategy(Strategy):
    """A `Strategy` that always chooses the `QuitSolver` to answer
    questions."""

    def get_solver(self, game_variables: dict, status: GameStatus) -> Solver:
        """Chooses to quit the question.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.
            status (GameStatus): The current game status (e.g. number of lives)

        Returns:
            tuple[str, QuestionOutcome]: A tuple of 'q' and the 'Incorrect' outcome.
        """
        return QuitSolver()
