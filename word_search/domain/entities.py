from dataclasses import dataclass, field

from word_search.domain.value_objects import ALL_DIRECTIONS, Direction


@dataclass
class PlacedWord:
    word: str
    x: int
    y: int
    xd: int
    yd: int


@dataclass
class Grid:
    width: int
    height: int
    data: list[str] = field(default_factory=list)
    used: list[str] = field(default_factory=list)
    placed_words: list[PlacedWord] = field(default_factory=list)

    def __post_init__(self):
        if not self.data:
            self.data = ["."] * (self.width * self.height)
        if not self.used:
            self.used = [" "] * (self.width * self.height)

    def _pos(self, x: int, y: int) -> int:
        return x + self.width * y

    def to_text(self) -> str:
        result = []
        for row in range(self.height):
            result.append("".join(self.data[row * self.width : (row + 1) * self.width]))
        return "\n".join(result)

    def can_place(self, word: str, x: int, y: int, xd: int, yd: int) -> bool:
        for i, c in enumerate(word):
            px, py = x + i * xd, y + i * yd
            if px < 0 or px >= self.width or py < 0 or py >= self.height:
                return False
            p = self._pos(px, py)
            if self.data[p] != "." and self.data[p] != c:
                return False
        return True

    def place_word(self, word: str, x: int, y: int, xd: int, yd: int) -> bool:
        if not self.can_place(word, x, y, xd, yd):
            return False
        for i, c in enumerate(word):
            px, py = x + i * xd, y + i * yd
            p = self._pos(px, py)
            self.data[p] = c
            self.used[p] = "."
        self.placed_words.append(PlacedWord(word, x, y, xd, yd))
        return True

    def fill_empty(self, pool: str) -> None:
        for i in range(len(self.data)):
            if self.data[i] == ".":
                self.data[i] = pool[i % len(pool)]


@dataclass
class Puzzle:
    grid: Grid
    words: list[str]
    puzzle_type: str


PUZZLE_STYLES = {
    "easy": (10, 10, (Direction(0, 1), Direction(1, 0))),
    "standard": (
        10,
        10,
        (
            Direction(1, 0),
            Direction(0, 1),
            Direction(1, 1),
            Direction(1, -1),
            Direction(-1, 1),
            Direction(-1, 0),
        ),
    ),
    "hard": (12, 12, tuple(ALL_DIRECTIONS)),
}
