import os

PUZZLES_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "puzzles")

CHARACTER_BUDGET = 66

MAX_WORD_LENGTH = {
    "letters": 10,
    "chinese": 10,
    "numbers": 4,
    "shapes": 4,
}

ALL_DIRECTIONS = ("+-", "+.", "++", ".+", ".-", "--", "-.", "-+")

STYLES = {
    "easy": ("10x10", ("+.", ".+")),
    "standard": ("10x10", ("+-", "+.", "++", ".+", ".-", "-.")),
    "hard": ("12x12", ALL_DIRECTIONS),
    "ying yang": ("10x10", ("+.", "++", ".+, +-")),
}

DIR_CONV = {
    "-": -1,
    ".": 0,
    "+": 1,
}

LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SHAPES = "◊●♠♣♥▲▼*%#@"

WORD_CATEGORIES = ["meat", "plants", "sports", "travel", "fruits", "animals"]
PUZZLE_TYPES = ["letters", "numbers", "chinese"]
