import os

import numpy as np

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
)


def retrieve_words(
    num_of_words: int,
    category: str,
    max_length: int = 10,
    character_budget: int = 66,
) -> list[str]:
    path = os.path.join(DATA_DIR, f"{category}.txt")
    with open(path) as f:
        words = [line.strip().lower() for line in f]
    words = [w for w in words if len(w) <= max_length]

    for _ in range(100):
        indices = np.random.choice(len(words), num_of_words, replace=False)
        selected = [words[i] for i in indices]
        if sum(len(w) for w in selected) <= character_budget:
            return selected
    return []


def retrieve_chinese_words(
    num_of_words: int,
    max_length: int = 10,
    character_budget: int = 66,
) -> list[str]:
    path = os.path.join(DATA_DIR, "chinese_idioms.txt")
    with open(path) as f:
        words = [line.strip() for line in f]
    words = [w for w in words if len(w) <= max_length]

    for _ in range(100):
        indices = np.random.choice(len(words), num_of_words, replace=False)
        selected = [words[i] for i in indices]
        if sum(len(w) for w in selected) <= character_budget:
            return selected
    return []


def generate_numbers(num: int, max_length: int = 4, fixed: bool = False) -> list[str]:
    out = []
    for _ in range(num):
        if fixed:
            value = np.random.randint(10 ** (max_length - 1), 10**max_length)
        else:
            digits = np.random.randint(1, max_length + 1)
            value = np.random.randint(10 ** (digits - 1), 10**digits)
        out.append(str(value))
    return out


def generate_shapes(num: int, max_length: int = 4) -> list[str]:
    shapes = "◊●♠♣♥▲▼*%#@"
    out = []
    for _ in range(num):
        digits = np.random.randint(1, max_length + 1)
        chars = [np.random.choice(list(shapes)) for _ in range(digits)]
        out.append("".join(chars))
    return out


def get_words_for_type(
    puzzle_type: str,
    num_words: int,
    category: str | None = None,
    max_length: int = 10,
    random_numbers: bool = True,
) -> list[str]:
    if puzzle_type == "letters":
        return retrieve_words(num_words, category or "animals", max_length)
    if puzzle_type == "numbers":
        return generate_numbers(num_words, max_length, not random_numbers)
    if puzzle_type == "chinese":
        return retrieve_chinese_words(num_words, max_length)
    if puzzle_type == "shapes":
        return generate_shapes(num_words, max_length)
    return []
