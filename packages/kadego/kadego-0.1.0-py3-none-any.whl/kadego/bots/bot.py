# Standard Library Imports
import asyncio

# Third-Party Imports
from playwright.async_api import Page

# Local Imports
from ..exceptions.invalid_bot_configuration_error import InvalidBotConfigurationError
from ..loggers.base_logger import BaseLogger
from ..loggers.logger import Logger
from ..strategies.strategy import Strategy
from ..utils.game_status import GameStatus
from ..utils.playwright import get_game_variables, press_key, press_key_sequence
from ..utils.question_outcome import QuestionOutcome
from ..world_maps.kanji_de_go_map import KanjiDeGoMap
from ..world_maps.world_map import WorldMap

SHORT = .1
MEDIUM = 1
LONG = 10
SOLUTION = 1


class Bot:
    """A class for automating the process of playing 漢字でGO!.

    A `Bot` can navigate to a given mode and level using a given `WorldMap`
    and set the number of lives and questions accordingly. It can also then
    play through rounds by answering questions using the specified `Strategy`.
    Additonally, question data can be logged by a given `Logger`.
    """
    def __init__(
            self,
            kadego: Page,
            mode: str,
            level: str,
            strategy: Strategy,
            lives: int = 5,
            questions: int = 16,
            logger: Logger | None = None,
            world_map: WorldMap | None = None,
            speed: float = 1.
    ) -> None:
        """Initializes the bot with necessary parameters.

        Args:
            kadego (Page): The Playwright page for playing 漢字でGO!.
            mode (str): The mode to play.
            level (str): The level to play.
            strategy (Strategy): The strategy for answering questions.
            lives (int, optional): The number of lives to set.
            questions (int, optional): The number of questions to set (default is 16).
            logger (Logger, optional): The logger to use (default is `BaseLogger`).
            world_map (WorldMap, optional): The world map to use (default is `KanjiDeGoMap`).
            speed (float, optional): The speed multiplier for bot actions (default is 1.0).
        """
        self.kadego: Page = kadego
        self.mode: str = mode
        self.level: str = level
        self.strategy: Strategy = strategy
        self.lives: int = lives
        self.questions: int = questions
        self.logger: Logger = logger or BaseLogger()
        self.world_map: WorldMap = world_map or KanjiDeGoMap()
        self.speed: float = speed

        self.game_status: GameStatus = GameStatus(0, 0)
        self.status: str = "Initialized"

        self._validate()

    def _validate(self) -> None:
        """Check if the bot's configuration is valid."""
        if self.mode not in self.world_map.modes:
            raise InvalidBotConfigurationError(f"Invalid mode: {self.mode}")

        if self.level not in self.world_map.mode_levels.get(self.mode, []):
            raise InvalidBotConfigurationError(f"Invalid level: {self.level} for mode: {self.mode}")

        if not (0 < self.lives < 6):
            raise InvalidBotConfigurationError(f"Invalid number of lives: {self.lives}. Must be between 1 and 5.")

        if self.questions not in (7, 10, 16):
            raise InvalidBotConfigurationError(f"Invalid number of questions: {self.questions}. Must be 7, 10, or 16.")

    def _get_new_game_status(self) -> GameStatus:
        """Returns a new game status object based on the specified lives and
        questions.

        Returns:
            GameStatus: A new game status object.
        """
        return GameStatus(self.lives, self.questions)

    async def _wait(self, delay: float) -> None:
        """Pauses the bot for a specified amount of time, scaled by the bot's
        speed.

        Args:
            delay (float): The time to wait in seconds.
        """
        await asyncio.sleep(delay * self.speed)

    async def _start_game(self) -> None:
        """Starts the game."""
        self.status = "Waiting for game to start"
        selector = "#_111_input"
        await self.kadego.wait_for_selector(selector)
        await self.kadego.press(selector, "Enter")
        await self._wait(LONG)

    async def _click_through_popups(self) -> None:
        """Clicks through the popups at the start of the game."""
        self.status = "Clicking through popups"
        keys = self.world_map.get_popups()
        await press_key_sequence(self.kadego, keys, MEDIUM)
        await self._wait(LONG)

    async def _navigate_to_mode(self) -> None:
        """Navigates to the specified mode."""
        self.status = f"Navigating to mode '{self.mode}'"
        keys = self.world_map.get_mode_direction(self.mode) * ["ArrowRight"]
        await press_key_sequence(self.kadego, keys, SHORT)

    async def _enter_mode(self) -> None:
        """Enters the specified mode."""
        self.status = f"Entering mode '{self.mode}'"
        await press_key(self.kadego, "Enter")
        await self._wait(MEDIUM)

    async def _click_through_mode_popups(self) -> None:
        """Clicks through the popups of the mode."""
        self.status = "Clicking through mode popups"
        keys = self.world_map.get_mode_popups(self.mode)
        await press_key_sequence(self.kadego, keys, MEDIUM)
        await self._wait(MEDIUM)

    async def _navigate_to_level(self) -> None:
        """Navigates to the specified level."""
        self.status = f"Navigating to level '{self.level}'"
        keys = self.world_map.get_level_direction(self.mode, self.level) * ["ArrowRight"]
        await press_key_sequence(self.kadego, keys, SHORT)
        await self._wait(MEDIUM)

    async def _set_lives(self) -> None:
        """Sets the number of lives."""
        self.status = f"Setting lives to '{self.lives}'"
        await press_key(self.kadego, "ArrowDown")
        await self._wait(MEDIUM)
        keys = 2 * ["ArrowDown"] + (self.lives - 1) * ["ArrowRight"] + ["Enter", "Shift"]
        await press_key_sequence(self.kadego, keys, SHORT)
        await self._wait(MEDIUM)

    async def _enter_level(self) -> None:
        """Enters the specified level."""
        self.status = f"Entering level '{self.level}'"
        await press_key(self.kadego, "Enter")
        await self._wait(MEDIUM)

    async def _click_through_level_popups(self) -> None:
        """Clicks through the popups of the level."""
        self.status = "Clicking through mode popups"
        keys = self.world_map.get_mode_level_popups(self.mode, self.level)
        await press_key_sequence(self.kadego, keys, MEDIUM)
        await self._wait(MEDIUM)

    async def _set_questions(self) -> None:
        """Sets the number of questions."""
        self.status = f"Setting questions to '{self.questions}'"
        keys = {7: 2, 10: 1, 16: 0}[self.questions] * ["ArrowUp"]
        await press_key_sequence(self.kadego, keys, SHORT)
        await self._wait(MEDIUM)

    async def _start_round(self) -> None:
        """Starts a round."""
        self.status = "Starting level"
        await press_key(self.kadego, "Enter")

    async def _wait_for_round_to_load(self) -> bool:
        """Waits for some time for the round to load.

        Returns:
            bool: True if the round loaded in time, False if it　did not.
        """
        selector = "#_111_input"
        for _ in range(60):
            element = await self.kadego.query_selector(selector)
            if element:
                return True
            await press_key(self.kadego, "Space")
            await self._wait(MEDIUM)
        return False

    async def _wait_for_question(self) -> None:
        """Waits for the next question."""
        self.status = "Waiting for question"
        selector = "#_111_input"
        await self.kadego.wait_for_selector(selector)

    async def _get_answer(self) -> tuple[str, QuestionOutcome]:
        """Retrieves an answer to the current question using the selected
        strategy.

        Returns:
            tuple[str, QuestionOutcome]: The answer and the　outcome of the question.
        """
        game_variables = await get_game_variables(self.kadego)
        answer, outcome = self.strategy.solve(game_variables, self.game_status)
        return answer, outcome

    async def _answer_question(self, answer: str, outcome: QuestionOutcome) -> None:
        """Provides an answer to the current question and updates the game
        status according to the provided outcome.

        Args:
            answer (str): The answer to submit.
            outcome　(QuestionOutcome): The outcome of the question.
        """
        self.status = f"Answering question with '{answer}'"
        selector = "#_111_input"
        await self.kadego.fill(selector, answer)
        await self.kadego.press(selector, "Enter")
        self.game_status.update(outcome)

    async def _wait_for_solution(self, outcome: QuestionOutcome) -> None:
        """Waits for the solution to be displayed and logs the current game
        state.

        Args:
            outcome (QuestionOutcome): The outcome of the question.
        """
        self.status = f"Waiting for solution"
        await self._wait(SOLUTION)
        game_variables = await get_game_variables(self.kadego)
        self.logger.log(game_variables)
        if not outcome.skipped and not outcome.correct:
            await press_key(self.kadego, "Space")

    async def _wait_for_round_reload_loop(self) -> None:
        """Waits for a new round to start, reloading the game if stuck."""
        self.status = "Waiting for round to load"
        self.game_status: GameStatus = self._get_new_game_status()
        ok = await self._wait_for_round_to_load()
        while not ok:
            await self.reload()
            ok = await self._wait_for_round_to_load()

    async def _answer_questions_loop(self) -> None:
        """Waits for and answers questions in a loop until the game is
        finished."""
        while not self.game_status.is_done():
            await self._wait_for_question()
            answer, outcome = await self._get_answer()
            await self._answer_question(answer, outcome)
            await self._wait_for_solution(outcome)

    async def _wait_for_round_to_finish(self) -> None:
        """Waits a little at the end of a round for e.g. the boss defeated
        animation to finish."""
        self.status = "Waiting for game to finish"
        if self.game_status.is_win():
            await self._wait(LONG)
        else:
            await self._wait(SHORT)

    async def _retry(self) -> None:
        """Starts a new round by retrying."""
        self.status = "Retrying"
        keys = 2 * ["ArrowDown"]
        await press_key_sequence(self.kadego, keys, SHORT)
        self.game_status = self._get_new_game_status()

    async def launch(self) -> None:
        """Navigates through the game performing all necessary setup and
        finally starts a round."""
        await self._start_game()
        await self._click_through_popups()
        await self._navigate_to_mode()
        await self._enter_mode()
        await self._click_through_mode_popups()
        await self._navigate_to_level()
        await self._set_lives()
        await self._enter_level()
        await self._click_through_level_popups()
        await self._set_questions()
        await self._start_round()

    async def reload(self) -> None:
        """Reloads the game and starts a new round again."""
        await self.kadego.reload()
        await self._start_game()
        await self._enter_mode()
        await self._enter_level()
        await self._start_round()

    async def run(self) -> None:
        """Runs the bot for one round of play."""
        await self._wait_for_round_reload_loop()
        await self._answer_questions_loop()
        await self._wait_for_round_to_finish()
        await self._retry()
