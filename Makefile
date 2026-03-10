.PHONY: install lint format run test clean

install:
	uv sync

lint:
	uv run ruff check --fix .
	uv run ruff check --select I --fix .

format:
	uv run ruff format .

run:
	uv run python __main__.py

test:
	uv run pytest -v

test-cov:
	uv run pytest

clean:
	rm -rf .ruff_cache
	rm -rf puzzles/*.pdf
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
