# Standard Library Imports
from dataclasses import dataclass


@dataclass
class QuestionOutcome:
    """A class representing the outcome of a question being answered.

    Attributes:
        correct (bool): Indicates whether the question was answered correctly.
        skipped (bool): Indicates whether the question was skipped.
    """

    correct: bool
    skipped: bool
