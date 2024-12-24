# Local Imports
from .world_map import WorldMap

MODES = {"main": 1, "casual": 2, "rush": 3, "extra": 4}

MAIN_LEVELS = {"normal": 0, "hard": 1, "very_hard": 2, "hell": 3}
CASUAL_LEVELS = {
    "basic": 0,
    "variety": 1,
    "variety_hard": 2,
    "one_character": 3,
    "four_characters": 4,
    "places": 5,
    "bugs": 6,
    "mammals": 7,
    "birds": 8,
    "aquatic": 9,
    "plants": 10,
    "food": 11,
}
RUSH_LEVELS = {
    "level_1": 0,
    "level_2": 1,
    "level_3": 2,
    "level_4": 3,
    "level_5": 4,
    "level_6": 5,
}
EXTRA_LEVELS = {"math": 0, "math_hard": 1, "english": 2, "elements": 3}
MODE_LEVELS = {
    "main": MAIN_LEVELS,
    "casual": CASUAL_LEVELS,
    "rush": RUSH_LEVELS,
    "extra": EXTRA_LEVELS,
}

POPUPS = ["Space", "Shift", "Space", "Shift", "Space"]
MODE_POPUPS = {"main": ["Space"]}
MODE_LEVEL_POPUPS = {"main": {"hell": ["Space"]}}


class KanjiDeGoMap(WorldMap):
    """A `WorldMap` of 漢字でGO!."""

    def __init__(self) -> None:
        """Initializes the WorldMap of 漢字でGO!"""
        super().__init__(MODES, MODE_LEVELS, POPUPS, MODE_POPUPS)
