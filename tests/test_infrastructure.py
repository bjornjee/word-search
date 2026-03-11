import os
import tempfile

from word_search.domain.entities import Grid, Puzzle
from word_search.infrastructure.pdf_generator import build_pdf
from word_search.infrastructure.word_repository import (
    generate_numbers,
    generate_shapes,
    get_words_for_type,
    retrieve_chinese_words,
    retrieve_words,
)


class TestWordRepository:
    def test_retrieve_words(self):
        words = retrieve_words(5, "animals", min_length=3, max_length=10)
        assert len(words) == 5
        assert all(3 <= len(w) <= 10 for w in words)

    def test_retrieve_words_character_budget(self):
        words = retrieve_words(
            5, "animals", min_length=3, max_length=10, character_budget=30
        )
        total = sum(len(w) for w in words)
        assert total <= 30

    def test_retrieve_chinese_words(self):
        words = retrieve_chinese_words(5, max_length=10)
        assert len(words) <= 5

    def test_generate_numbers_random(self):
        numbers = generate_numbers(5, min_length=3, max_length=6, fixed=False)
        assert len(numbers) == 5
        for num in numbers:
            assert 3 <= len(num) <= 6

    def test_generate_numbers_fixed(self):
        numbers = generate_numbers(5, min_length=3, max_length=6, fixed=True)
        assert len(numbers) == 5
        for num in numbers:
            assert len(num) == 6

    def test_generate_shapes(self):
        shapes = generate_shapes(5, min_length=2, max_length=4)
        assert len(shapes) == 5
        for shape in shapes:
            assert 2 <= len(shape) <= 4

    def test_get_words_for_type_letters(self):
        words = get_words_for_type(
            "letters",
            5,
            "animals",
            min_length=3,
            max_length=10,
            budget=50,
            random_numbers=True,
        )
        assert len(words) <= 5

    def test_get_words_for_type_numbers(self):
        words = get_words_for_type(
            "numbers",
            5,
            None,
            min_length=3,
            max_length=6,
            budget=60,
            random_numbers=True,
        )
        assert len(words) == 5

    def test_get_words_for_type_chinese(self):
        words = get_words_for_type(
            "chinese",
            5,
            None,
            min_length=2,
            max_length=10,
            budget=40,
            random_numbers=True,
        )
        assert len(words) <= 5

    def test_retrieve_words_no_matching_words(self):
        words = retrieve_words(5, "animals", min_length=100, max_length=200)
        assert len(words) == 0

    def test_retrieve_words_more_than_available(self):
        words = retrieve_words(1000, "animals", min_length=3, max_length=10)
        assert len(words) == 0

    def test_retrieve_words_tight_budget(self):
        words = retrieve_words(
            10, "animals", min_length=3, max_length=7, character_budget=30
        )
        assert len(words) <= 10
        assert sum(len(w) for w in words) <= 30

    def test_retrieve_chinese_words_tight_budget(self):
        words = retrieve_chinese_words(
            10, min_length=3, max_length=4, character_budget=30
        )
        assert len(words) <= 10

    def test_generate_numbers_tight_budget(self):
        numbers = generate_numbers(10, min_length=3, max_length=4, character_budget=30)
        assert len(numbers) <= 10

    def test_generate_shapes_tight_budget(self):
        shapes = generate_shapes(10, min_length=2, max_length=3, character_budget=15)
        assert len(shapes) <= 10

    def test_retrieve_words_greedy_resample(self):
        words = retrieve_words(
            10, "animals", min_length=3, max_length=7, character_budget=31
        )
        assert len(words) == 10
        assert sum(len(w) for w in words) <= 31

    def test_get_words_for_type_unknown(self):
        words = get_words_for_type("unknown_type", 5, None, 3, 10, 50, True)
        assert len(words) == 0


class TestPdfGenerator:
    def test_build_pdf_creates_file(self):
        grid = Grid(10, 10)
        grid.place_word("test", 0, 0, 1, 0)
        grid.fill_empty("abcdefghij")
        puzzle = Puzzle(grid=grid, words=["test"], puzzle_type="letters")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            filename = f.name

        try:
            build_pdf(puzzle, filename)
            assert os.path.exists(filename)
            assert os.path.getsize(filename) > 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_build_pdf_letters(self):
        grid = Grid(10, 10)
        grid.place_word("cat", 0, 0, 1, 0)
        grid.fill_empty("abcdefghij")
        puzzle = Puzzle(grid=grid, words=["cat", "dog"], puzzle_type="letters")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            filename = f.name

        try:
            build_pdf(puzzle, filename)
            assert os.path.exists(filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_build_pdf_numbers(self):
        grid = Grid(10, 10)
        grid.place_word("12", 0, 0, 1, 0)
        grid.fill_empty("0123456789")
        puzzle = Puzzle(grid=grid, words=["12", "34"], puzzle_type="numbers")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            filename = f.name

        try:
            build_pdf(puzzle, filename)
            assert os.path.exists(filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
