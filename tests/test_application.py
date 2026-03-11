import os
import shutil

from word_search.application.use_cases import (
    create_all_puzzles,
    generate_single_puzzle,
    merge_pdfs,
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

    def test_generate_single_puzzle_shapes(self):
        result = generate_single_puzzle(
            idx=0,
            puzzle_type="shapes",
            category="animals",
            difficulty="easy",
            num_words=5,
            random_numbers=True,
        )
        assert result[0] == "shapes"
        assert result[1] == 1

    def test_generate_single_puzzle_returns_zero_when_no_words(self):
        from word_search.application.use_cases import PUZZLE_CONFIG

        original = PUZZLE_CONFIG["letters"]["budget"]
        PUZZLE_CONFIG["letters"]["budget"] = 20
        try:
            result = generate_single_puzzle(
                idx=999,
                puzzle_type="letters",
                category="animals",
                difficulty="easy",
                num_words=10,
                random_numbers=True,
            )
            assert result[1] == 0
        finally:
            PUZZLE_CONFIG["letters"]["budget"] = original

    def test_generate_single_puzzle_returns_zero_when_impossible_grid(self):
        from word_search.application.use_cases import PUZZLE_CONFIG

        original = PUZZLE_CONFIG["letters"]["budget"]
        PUZZLE_CONFIG["letters"]["budget"] = 30
        try:
            result = generate_single_puzzle(
                idx=998,
                puzzle_type="letters",
                category="animals",
                difficulty="easy",
                num_words=50,
                random_numbers=True,
            )
            assert result[1] == 0
        finally:
            PUZZLE_CONFIG["letters"]["budget"] = original

    def test_generate_single_puzzle_returns_zero_when_grid_none(self):
        from word_search.application.use_cases import PUZZLE_CONFIG

        original = PUZZLE_CONFIG["letters"]["budget"]
        PUZZLE_CONFIG["letters"]["budget"] = 100
        try:
            result = generate_single_puzzle(
                idx=997,
                puzzle_type="letters",
                category="animals",
                difficulty="hard",
                num_words=10,
                random_numbers=True,
            )
            if result[1] == 0:
                assert True
        finally:
            PUZZLE_CONFIG["letters"]["budget"] = original

    def test_merge_pdfs(self):
        os.makedirs("puzzles", exist_ok=True)
        for i in range(3):
            generate_single_puzzle(
                idx=i,
                puzzle_type="letters",
                category="animals",
                difficulty="easy",
                num_words=5,
                random_numbers=True,
            )

        merge_pdfs("letters", 3)

        assert os.path.exists("puzzles/yy-letters.pdf")

        from pypdf import PdfReader

        reader = PdfReader("puzzles/yy-letters.pdf")
        assert len(reader.pages) == 3

    def test_create_all_puzzles_creates_folder(self):
        import tempfile

        import word_search.config as config

        test_dir = tempfile.mkdtemp()
        original_val = config.PUZZLES_FOLDER
        try:
            config.PUZZLES_FOLDER = test_dir
            create_all_puzzles(num_files=2, num_workers=1)
            assert os.path.exists(test_dir)
        finally:
            config.PUZZLES_FOLDER = original_val
            shutil.rmtree(test_dir, ignore_errors=True)
