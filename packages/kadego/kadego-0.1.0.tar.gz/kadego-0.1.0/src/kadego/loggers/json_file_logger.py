# Standard Library Imports
import json
from abc import abstractmethod

# Local Imports
from .logger import Logger


class JsonFileLogger(Logger):
    """An Abstract base class for logging game variables into a JSON file.

    This `Logger` temporarily stores the data from the game variables and
    writes it into a JSON file.
    """

    def __init__(self, path: str) -> None:
        """Initializes the logger.

        Args:
            path (str): The path to the JSON file where log data will be stored.
        """
        super().__init__()
        self.path: str = path
        self.data: dict = self._read_data()

    def _read_data(self) -> dict:
        """Reads data from the specified JSON file.

        Returns:
            dict: The data read from the JSON file.
        """
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return dict()

    def _write_data(self) -> None:
        """Writes the current log data to the specified JSON file."""
        data_lines = [f'  "{key}": {json.dumps(value, ensure_ascii=False)}' for key, value in self.data.items()]
        data_string = "{\n" + ",\n".join(data_lines) + "\n}"

        with open(self.path, "w", encoding="utf-8") as file:
            file.write(data_string)

    @abstractmethod
    def log(self, game_variables: dict) -> None:
        """Logs the given game variables to be written into a JSON file.

        Args:
            game_variables (dict): The game variables shortly after a solution was revealed.
        """
        pass
