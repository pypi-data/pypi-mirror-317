Modes = dict[str, int]
ModeLevels = dict[str, dict[str, int]]
Popups = list[str]
ModePopups = dict[str, Popups]
ModeLevelPopups = dict[str, dict[str, Popups]]


class WorldMap:
    """A class representing a world map of a game.

    A `WorldMap` consists of different modes which in turn have levels. Each of
    these has a location which represents the amount of right arrow button
    presses it would take to get there. Additionally, the game in general, each
    mode and each level in a mode can have a number of popups which appear.
    """

    def __init__(
        self,
        modes: Modes,
        mode_levels: ModeLevels,
        popups: Popups | None = None,
        mode_popups: ModePopups | None = None,
        mode_level_popups: ModeLevelPopups | None = None,
    ) -> None:
        """Initializes the WorldMap.

        Args:
            modes (Modes): A dictionary specifying the mode locations.
            mode_levels (ModeLevels): A dictionary specifying the level locations.
            popups (Popups, optional): A list of popups (default is list()).
            mode_popups (ModePopups, optional): A dictionary specifying the mode popups (default is dict()).
            mode_level_popups (ModeLevelPopups, optional): A dictionary specifying the level popups (default is dict()).
        """
        self.modes: Modes = modes
        self.mode_levels: ModeLevels = mode_levels
        self.popups: Popups = popups or []
        self.mode_popups: ModePopups = mode_popups or dict()
        self.mode_level_popups: ModeLevelPopups = mode_level_popups or dict()

    def get_mode_direction(self, mode: str) -> int:
        """Retrieves the location of a mode.

        Args:
            mode (str): The mode for which the location is requested.

        Returns:
            int: The amount of right arrow button presses necessary to get to the location.
        """
        return self.modes[mode]

    def get_level_direction(self, mode: str, level: str) -> int:
        """Retrieves the location of a level in a mode.

        Args:
            mode (str): The mode of the given level.
            level (str): The level for which the location is requested.

        Returns:
            int: The amount of right arrow button presses necessary to get to the level.
        """
        return self.mode_levels[mode][level]

    def get_popups(self) -> Popups:
        """Gives instructions on how to close popups.

        Returns:
            Popups: The list of button presses necessary to close the popups.
        """
        return self.popups

    def get_mode_popups(self, mode: str) -> Popups:
        """Gives instructions on how to close popups in a mode.

        Args:
            mode (str): The mode in which the popups appear.

        Returns:
            Popups: The list of button presses necessary to close the popups.
        """
        return self.mode_popups.get(mode) or []

    def get_mode_level_popups(self, mode: str, level: str) -> Popups:
        """Gives instructions on how to close popups in a level of a mode.

        Args:
            mode (str): The mode of the given level.
            level (str): The level in which the popups appear.

        Returns:
            Popups: The list of button presses necessary to close the popups.
        """
        level_popups = self.mode_level_popups.get(mode)
        if level_popups is None:
            return []
        return level_popups.get(level) or []
