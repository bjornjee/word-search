import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed

from pypdf import PdfReader, PdfWriter

from word_search.config import PUZZLES_FOLDER, WORD_CATEGORIES
from word_search.domain import fill_grid, generate_grid
from word_search.infrastructure import build_pdf, get_words_for_type

PUZZLE_CONFIG = {
    "letters": {"min_length": 3, "max_length": 7, "budget": 70},
    "numbers": {"min_length": 3, "max_length": 6, "budget": 50},
    "chinese": {"min_length": 2, "max_length": 6, "budget": 65},
    "shapes": {"min_length": 2, "max_length": 4, "budget": 50},
}


def generate_single_puzzle(
    idx: int,
    puzzle_type: str,
    category: str,
    difficulty: str,
    num_words: int,
    random_numbers: bool,
) -> tuple[str, int]:
    config = PUZZLE_CONFIG.get(
        puzzle_type, {"min_length": 3, "max_length": 10, "budget": 50}
    )

    words = get_words_for_type(
        puzzle_type,
        num_words,
        category,
        min_length=config["min_length"],
        max_length=config["max_length"],
        budget=config["budget"],
        random_numbers=random_numbers,
    )

    if not words:
        return puzzle_type, 0

    grid = generate_grid(words, difficulty)
    if grid is None:
        return puzzle_type, 0

    puzzle = fill_grid(grid, words, puzzle_type)

    filename = os.path.join(PUZZLES_FOLDER, f"{puzzle_type}_{idx}.pdf")
    build_pdf(puzzle, filename)
    return puzzle_type, 1


def merge_pdfs(puzzle_type: str, count: int) -> None:
    files = [
        os.path.join(PUZZLES_FOLDER, f"{puzzle_type}_{i}.pdf") for i in range(count)
    ]

    writer = PdfWriter()
    for file in files:
        if os.path.exists(file):
            reader = PdfReader(file)
            for page in reader.pages:
                writer.add_page(page)
            os.remove(file)

    output_path = os.path.join(PUZZLES_FOLDER, f"yy-{puzzle_type}.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)


def create_all_puzzles(num_files: int = 200, num_workers: int = 4) -> None:
    if not os.path.exists(PUZZLES_FOLDER):
        os.makedirs(PUZZLES_FOLDER)
    elif os.listdir(PUZZLES_FOLDER):
        shutil.rmtree(PUZZLES_FOLDER)
        os.makedirs(PUZZLES_FOLDER)

    puzzle_types = ["letters", "numbers", "chinese"]

    for puzzle_type in puzzle_types:
        tasks = []
        for i in range(num_files):
            category = WORD_CATEGORIES[i % len(WORD_CATEGORIES)]
            tasks.append(
                {
                    "idx": i,
                    "puzzle_type": puzzle_type,
                    "category": category,
                    "difficulty": "hard",
                    "num_words": 10,
                    "random_numbers": True,
                }
            )

        results = []
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(generate_single_puzzle, **task) for task in tasks
            ]
            for future in as_completed(futures):
                results.append(future.result())

        success_count = sum(1 for _, r in results if r == 1)
        merge_pdfs(puzzle_type, num_files)
        print(f"{puzzle_type}: {success_count}/{num_files} puzzles created")
