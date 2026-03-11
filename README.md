# Word Search Generator

A Python tool to generate word search puzzles in PDF format with support for English words, numbers, and Chinese characters.

## Features

- **Multiple puzzle types**: Letters, numbers, Chinese characters, and shapes
- **Difficulty levels**: Easy, standard, and hard (varying grid sizes and word directions)
- **Configurable**: Adjustable word count, length, and character budget per puzzle type
- **PDF output**: Clean, printable puzzles with word lists

## Example

![Word Search Example](exmaple.png)

## Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) (for managing Python environments and dependencies)

### Installation

```bash
git clone https://github.com/bjornjee/word-search.git
cd word-search
make install
```

### Running the Generator

```bash
make run
```

This generates 200 puzzles of each type (letters, numbers, chinese) in the `puzzles/` directory.

### Cleaning Up

```bash
make clean
```

## Development

```bash
make test      # Run tests
make test-cov  # Run tests with coverage
make lint      # Run linter
```
