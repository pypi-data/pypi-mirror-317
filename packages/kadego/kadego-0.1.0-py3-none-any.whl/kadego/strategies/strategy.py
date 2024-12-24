# Standard Library Imports
from abc import ABC, abstractmethod

# Local Imports
from ..solvers.solver import Solver
from ..utils.game_status import GameStatus
from ..utils.question_outcome import QuestionOutcome


class Strategy(ABC):
    """An abstract base class for solving questions base on the current game
    status.

    A `Strategy` answers questions getting an answer from an appropriate
    `Solver` based on the current game status.
    """

    def __init__(self) -> None:
        """Initializes the strategy."""
        return

    @abstractmethod
    def get_solver(self, game_variables: dict, status: GameStatus) -> Solver:
        """Chooses the appropriate solver based on the game variables and
        current game status.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.
            status (GameStatus): The current game status (e.g. number of lives)

        Returns:
            Solver: The choosen solver to answer the question.
        """
        pass

    def solve(self, game_variables: dict, status: GameStatus) -> tuple[str, QuestionOutcome]:
        """Solves the question by getting an answer from the appropriate solver.

        Args:
            game_variables (dict): The game variables shortly after a question was posed.
            status (GameStatus): The current game status (e.g. number of lives)

        Returns:
            tuple[str, QuestionOutcome]: A tuple of the chosen answer and the corresponding outcome.
        """
        solver = self.get_solver(game_variables, status)
        return solver.solve(game_variables)
