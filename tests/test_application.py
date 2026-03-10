import os

from word_search.application.use_cases import (
    generate_single_puzzle,
)


class TestUseCases:
    def test_generate_single_puzzle_letters(self):
        result = generate_single_puzzle(
            idx=0,
            puzzle_type="letters",
            category="animals",
            difficulty="easy",
            num_words=5,
            random_numbers=True,
        )
        assert result[0] == "letters"
        assert result[1] == 1
        assert os.path.exists(os.path.join("puzzles", "letters_0.pdf"))

    def test_generate_single_puzzle_numbers(self):
        result = generate_single_puzzle(
            idx=0,
            puzzle_type="numbers",
            category="animals",
            difficulty="easy",
            num_words=5,
            random_numbers=True,
        )
        assert result[0] == "numbers"
        assert result[1] == 1

    def test_generate_single_puzzle_chinese(self):
        result = generate_single_puzzle(
            idx=0,
            puzzle_type="chinese",
            category="animals",
            difficulty="easy",
            num_words=5,
            random_numbers=True,
        )
        assert result[0] == "chinese"
        assert result[1] == 1
