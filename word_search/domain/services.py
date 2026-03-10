import random
from collections.abc import Sequence

from word_search.domain.entities import PUZZLE_STYLES, Grid, Puzzle
from word_search.domain.value_objects import Direction


def generate_grid(
    words: Sequence[str],
    style: str = "standard",
    tries: int = 100,
) -> Grid | None:
    width, height, directions = PUZZLE_STYLES.get(style, PUZZLE_STYLES["standard"])
    words = sorted(words, key=len, reverse=True)
    grid = Grid(width, height)
    prev_dir = Direction(0, 0)

    for word in words:
        word_len = len(word)
        attempts = 0
        placed = False

        while attempts < tries:
            direction = random.choice(directions)
            xd, yd = direction.xd, direction.yd

            min_x = (word_len - 1, 0, 0)[xd + 1]
            max_x = (width - 1, width - 1, width - word_len)[xd + 1]
            min_y = (word_len - 1, 0, 0)[yd + 1]
            max_y = (height - 1, height - 1, height - word_len)[yd + 1]

            if min_x > max_x or min_y > max_y:
                attempts += 1
                continue

            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)

            if (xd, yd) != (prev_dir.xd, prev_dir.yd) and grid.place_word(
                word, x, y, xd, yd
            ):
                prev_dir = direction
                placed = True
                break
            attempts += 1

        if not placed:
            return None

    return grid


def fill_grid(grid: Grid, words: list[str], puzzle_type: str) -> Puzzle:
    pool_map = {
        "letters": "".join(w[:3] for w in words),
        "numbers": "0123456789",
        "chinese": "".join(w[:3] for w in words),
        "shapes": "◊●♠♣♥▲▼*%#@",
    }
    pool = pool_map.get(puzzle_type, "abcdefghijklmnopqrstuvwxyz")
    grid.fill_empty(pool)
    return Puzzle(grid=grid, words=list(words), puzzle_type=puzzle_type)
