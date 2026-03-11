from word_search.domain.entities import PUZZLE_STYLES, Grid, PlacedWord
from word_search.domain.services import fill_grid, generate_grid
from word_search.domain.value_objects import ALL_DIRECTIONS, Direction


class TestDirection:
    def test_direction_creation(self):
        d = Direction(1, 0)
        assert d.xd == 1
        assert d.yd == 0

    def test_direction_from_string(self):
        d = Direction.from_string("+-")
        assert d.xd == 1
        assert d.yd == -1

    def test_direction_iterator(self):
        d = Direction(1, 1)
        xd, yd = d
        assert xd == 1
        assert yd == 1

    def test_all_directions_count(self):
        assert len(ALL_DIRECTIONS) == 8


class TestPlacedWord:
    def test_placed_word_creation(self):
        pw = PlacedWord("test", 0, 0, 1, 0)
        assert pw.word == "test"
        assert pw.x == 0
        assert pw.y == 0
        assert pw.xd == 1
        assert pw.yd == 0


class TestGrid:
    def test_grid_creation(self):
        grid = Grid(10, 10)
        assert grid.width == 10
        assert grid.height == 10
        assert len(grid.data) == 100
        assert len(grid.used) == 100

    def test_grid_pos(self):
        grid = Grid(10, 10)
        assert grid._pos(0, 0) == 0
        assert grid._pos(5, 5) == 55
        assert grid._pos(9, 9) == 99

    def test_to_text(self):
        grid = Grid(3, 3)
        grid.data = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        text = grid.to_text()
        lines = text.split("\n")
        assert len(lines) == 3
        assert lines[0] == "abc"
        assert lines[1] == "def"
        assert lines[2] == "ghi"

    def test_can_place_valid(self):
        grid = Grid(10, 10)
        assert grid.can_place("test", 0, 0, 1, 0) is True

    def test_can_place_out_of_bounds(self):
        grid = Grid(5, 5)
        assert grid.can_place("test", 3, 0, 1, 0) is False

    def test_can_place_overlap_same_letter(self):
        grid = Grid(10, 10)
        grid.place_word("test", 0, 0, 1, 0)
        assert grid.can_place("test", 0, 0, 1, 0) is True

    def test_can_place_overlap_different_letter(self):
        grid = Grid(10, 10)
        grid.place_word("test", 0, 0, 1, 0)
        assert grid.can_place("best", 0, 0, 1, 0) is False

    def test_place_word_success(self):
        grid = Grid(10, 10)
        result = grid.place_word("test", 0, 0, 1, 0)
        assert result is True
        assert grid.data[0:4] == list("test")

    def test_place_word_failure(self):
        grid = Grid(10, 10)
        grid.place_word("test", 0, 0, 1, 0)
        result = grid.place_word("best", 0, 0, 1, 0)
        assert result is False

    def test_fill_empty(self):
        grid = Grid(3, 3)
        grid.data = ["a", ".", "b", ".", ".", ".", "c", ".", "."]
        grid.fill_empty("xyz")
        assert "x" in grid.data or "y" in grid.data or "z" in grid.data


class TestPuzzleStyles:
    def test_easy_style(self):
        width, height, directions = PUZZLE_STYLES["easy"]
        assert width == 10
        assert height == 10
        assert len(directions) == 2

    def test_standard_style(self):
        width, height, directions = PUZZLE_STYLES["standard"]
        assert width == 10
        assert height == 10
        assert len(directions) == 6

    def test_hard_style(self):
        width, height, directions = PUZZLE_STYLES["hard"]
        assert width == 12
        assert height == 12
        assert len(directions) == 8


class TestGenerateGrid:
    def test_generate_grid_basic(self):
        grid = generate_grid(["cat", "dog"], style="easy")
        assert grid is not None
        assert grid.width == 10
        assert grid.height == 10

    def test_generate_grid_returns_none_when_impossible(self):
        grid = generate_grid(["abcdefghijklmnopqrstuvwxyz"], style="easy", tries=1)
        assert grid is None

    def test_generate_grid_uses_all_words(self):
        words = ["cat", "dog", "bird"]
        grid = generate_grid(words, style="easy")
        assert grid is not None
        placed_words = [pw.word for pw in grid.placed_words]
        assert len(placed_words) == 3


class TestFillGrid:
    def test_fill_grid_letters(self):
        grid = Grid(10, 10)
        grid.place_word("cat", 0, 0, 1, 0)
        puzzle = fill_grid(grid, ["cat", "dog"], "letters")
        assert puzzle.puzzle_type == "letters"
        assert "." not in puzzle.grid.data

    def test_fill_grid_numbers(self):
        grid = Grid(10, 10)
        grid.place_word("12", 0, 0, 1, 0)
        puzzle = fill_grid(grid, ["12", "34"], "numbers")
        assert puzzle.puzzle_type == "numbers"
        assert "." not in puzzle.grid.data

    def test_fill_grid_chinese(self):
        grid = Grid(10, 10)
        grid.place_word("中文", 0, 0, 1, 0)
        puzzle = fill_grid(grid, ["中文", "测试"], "chinese")
        assert puzzle.puzzle_type == "chinese"
        assert "." not in puzzle.grid.data

    def test_fill_grid_raises_on_empty_words(self):
        grid = Grid(10, 10)
        grid.place_word("cat", 0, 0, 1, 0)
        try:
            fill_grid(grid, [], "letters")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "must not be empty" in str(e)
