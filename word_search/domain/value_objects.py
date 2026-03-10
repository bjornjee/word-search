from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Direction:
    xd: int
    yd: int

    @classmethod
    def from_string(cls, s: str) -> "Direction":
        dir_map = {"-": -1, ".": 0, "+": 1}
        return cls(dir_map[s[0]], dir_map[s[1]])

    def __iter__(self):
        yield self.xd
        yield self.yd


ALL_DIRECTIONS = [
    Direction(-1, 1),
    Direction(-1, 0),
    Direction(-1, -1),
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, -1),
    Direction(1, 0),
    Direction(1, 1),
]


@dataclass
class GridConfig:
    width: int
    height: int
    directions: tuple[Direction, ...]
