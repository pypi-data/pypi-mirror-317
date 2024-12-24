# Local Imports
from .strategy import Strategy
from ..solvers.correct_solver import CorrectSolver
from ..solvers.quit_solver import QuitSolver
from ..solvers.skip_solver import SkipSolver
from ..solvers.solver import Solver
from ..utils.game_status import GameStatus


class CuriousStrategy(Strategy):
    """A `Strategy` aims to maximize the amount of questions in a round."""

    def get_solver(self, game_variables: dict, status: GameStatus) -> Solver:
        """Selects to skip when possible and answer correctly otherwise. That
        is except for at the peniultimate question where it will select to
        quit until only one life remaining and on the last question where it
        will also choose to quit after skippingis no longer possible.

        Args:
             game_variables (dict): The game variables shortly after a question was posed.
             status (GameStatus): The current game status (e.g. number of lives)

         Returns:
             tuple[str, QuestionOutcome]: A tuple of the chosen answer and the corresponding outcome.
        """
        if status.skip:
            return SkipSolver()
        if status.question == status.questions - 1 and status.lives > 1:
            return QuitSolver()
        if status.question == status.questions and not status.skip:
            return QuitSolver()
        return CorrectSolver()
