import time

from word_search.application import create_all_puzzles


def main():
    start = time.perf_counter()
    create_all_puzzles(num_files=200, num_workers=4)
    print(time.perf_counter() - start)


if __name__ == "__main__":
    main()
