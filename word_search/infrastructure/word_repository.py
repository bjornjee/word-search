import os

import numpy as np

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data"
)


def retrieve_words(
    num_of_words: int,
    category: str,
    min_length: int = 3,
    max_length: int = 10,
    character_budget: int = 50,
) -> list[str]:
    path = os.path.join(DATA_DIR, f"{category}.txt")
    with open(path) as f:
        words = [line.strip().lower() for line in f]
    words = [w for w in words if min_length <= len(w) <= max_length]

    if not words or num_of_words > len(words):
        return []

    for _ in range(100):
        indices = np.random.choice(len(words), num_of_words, replace=False)
        selected = [words[i] for i in indices]
        total_chars = sum(len(w) for w in selected)

        if total_chars <= character_budget:
            return selected

        remaining_budget = character_budget - sum(len(w) for w in selected[:-1])
        if remaining_budget <= 0:
            continue

        valid_last_words = [w for w in words if len(w) <= remaining_budget]
        if valid_last_words:
            selected[-1] = np.random.choice(valid_last_words)
            return selected

    shorter_words = [w for w in words if len(w) <= character_budget // num_of_words]
    if len(shorter_words) >= num_of_words:
        indices = np.random.choice(len(shorter_words), num_of_words, replace=False)
        return [shorter_words[i] for i in indices]

    return []


def retrieve_chinese_words(
    num_of_words: int,
    min_length: int = 2,
    max_length: int = 10,
    character_budget: int = 40,
) -> list[str]:
    path = os.path.join(DATA_DIR, "chinese_idioms.txt")
    with open(path) as f:
        words = [line.strip() for line in f]
    words = [w for w in words if min_length <= len(w) <= max_length]

    if not words or num_of_words > len(words):
        return []

    for _ in range(100):
        indices = np.random.choice(len(words), num_of_words, replace=False)
        selected = [words[i] for i in indices]
        total_chars = sum(len(w) for w in selected)

        if total_chars <= character_budget:
            return selected

        remaining_budget = character_budget - sum(len(w) for w in selected[:-1])
        if remaining_budget <= 0:
            continue

        valid_last_words = [w for w in words if len(w) <= remaining_budget]
        if valid_last_words:
            selected[-1] = np.random.choice(valid_last_words)
            return selected

    shorter_words = [w for w in words if len(w) <= character_budget // num_of_words]
    if len(shorter_words) >= num_of_words:
        indices = np.random.choice(len(shorter_words), num_of_words, replace=False)
        return [shorter_words[i] for i in indices]

    return []


def generate_numbers(
    num: int,
    min_length: int = 3,
    max_length: int = 6,
    character_budget: int = 60,
    fixed: bool = False,
) -> list[str]:
    out = []
    for _ in range(num):
        if fixed:
            value = np.random.randint(10 ** (max_length - 1), 10**max_length)
        else:
            digits = np.random.randint(min_length, max_length + 1)
            value = np.random.randint(10 ** (digits - 1), 10**digits)
        out.append(str(value))
    return out


def generate_shapes(
    num: int,
    min_length: int = 2,
    max_length: int = 4,
    character_budget: int = 70,
) -> list[str]:
    shapes = "◊●♠♣♥▲▼*%#@"
    out = []
    for _ in range(num):
        digits = np.random.randint(min_length, max_length + 1)
        chars = [np.random.choice(list(shapes)) for _ in range(digits)]
        out.append("".join(chars))
    return out


def get_words_for_type(
    puzzle_type: str,
    num_words: int,
    category: str | None = None,
    min_length: int = 3,
    max_length: int = 10,
    budget: int = 50,
    random_numbers: bool = True,
) -> list[str]:
    if puzzle_type == "letters":
        return retrieve_words(
            num_words, category or "animals", min_length, max_length, budget
        )
    if puzzle_type == "numbers":
        return generate_numbers(
            num_words, min_length, max_length, budget, not random_numbers
        )
    if puzzle_type == "chinese":
        return retrieve_chinese_words(num_words, min_length, max_length, budget)
    if puzzle_type == "shapes":
        return generate_shapes(num_words, min_length, max_length, budget)
    return []
