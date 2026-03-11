# Agent Guidelines

## Parameter Tuning (Binary Search)

When tuning parameters like budget, min_length, max_length:

1. **Test the full pipeline** - Always test `generate_single_puzzle()` end-to-end, never intermediate functions in isolation

2. **Use sufficient sample size** - Minimum 500 random seeds to catch edge cases, check for 0 failures not just "most pass"

3. **Binary search range** - Start with conservative bounds, search between current-known-working and known-failing

4. **Verify with parallel execution** - Test with `num_workers=4` to catch concurrency issues; single-threaded success ≠ parallel success

5. **Validate output** - Check exact page counts match expected (200 per type); don't assume success from console output alone

## Code Quality Standards

### Error Handling
- **Never use silent fallbacks** to mask bugs. For example:
  - Empty word list → raise `ValueError`, don't use default pool
  - Missing configuration → fail fast with clear error

### Validation
- Always validate inputs early (e.g., `if not words: return puzzle_type, 0`)
- Words list MUST be non-empty - this is a basic requirement for the game

### Testing
- Minimum 90% test coverage
- Test both success and failure paths
- Tests should be self-contained and clean up after themselves
- Always run `make run` to validate end-to-end execution
- Verify page count is exactly 200 per puzzle type

## Implementation Patterns

### Hardened Selection Algorithm
When selecting words with a budget constraint:
1. Track cumulative character count
2. If last word exceeds budget, greedily resample from valid shorter words
3. Fallback to shorter words only if primary selection fails
4. Return empty list if no valid selection possible (don't mask with defaults)

### Configuration
- Use configuration dictionaries (e.g., `PUZZLE_CONFIG`) for related parameters
- Keep budgets optimized via binary search - maximize while maintaining 0 failures
- Budgets are per puzzle type, independent of word count

## Working Directory

All commands should run in `/Users/bjornjee/Code/bjornjee/word-search`

## Running Tests

```bash
make test      # Run tests
make test-cov  # Run tests with coverage
make lint      # Run linter
make run       # Generate puzzles
```
