# Standard Library Imports
from dataclasses import dataclass

# Local Imports
from ..utils.question_outcome import QuestionOutcome


@dataclass
class GameStatus:
    """A class representing the current status of the game and updates
    when given a `QuestionOutcome`.

    Attributes:
        lives (int): The number of lives remaining.
        questions (int): The total number of questions.
        question (int): The current question number.
        skip (bool): Flag indicating whether skipping is possible.
    """

    lives: int
    questions: int
    question: int = 1
    skip: bool = True

    def update(self, outcome: QuestionOutcome) -> None:
        """Updates the game status based on the outcome of a question.

        Args:
            outcome (QuestionOutcome): The outcome of the question
        """
        if outcome.skipped:
            self.skip = False
        elif outcome.correct:
            if self.question % (self.questions // 3) == 0:
                self.skip = True
            self.question += 1
        else:
            self.lives -= 1

    def is_done(self) -> bool:
        """Checks if the round is over.

        Returns:
            bool: True if not lives remain or the total number of questions was reached, False otherwise.
        """
        return self.lives == 0 or self.question > self.questions

    def is_win(self) -> bool:
        """Checks if the round was one.

        Returns:
            bool: True if the round is done and lives still remain, False otherwise.
        """
        return self.is_done() and self.lives > 0

    def is_loss(self) -> bool:
        """Checks if the round was one.

        Returns:
            bool: True if the round is done and not lives remain, False otherwise.
        """
        return self.is_done() and self.lives == 0
