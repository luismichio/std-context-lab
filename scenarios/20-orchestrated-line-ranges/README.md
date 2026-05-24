# Scenario 20: Line Range Precision & Fallbacks

## Objective
To stress test the slicing logic of `pipe_read_file` to ensure precise context retrieval and safe handling of boundary edge cases.

## Setup
- **Tool**: `pipe_read_file` (Orchestrated tool).
- **File**: `numbered_lines.txt` (1,000 lines with explicit line numbers).
- **Edge Cases**: Out-of-Bounds (High), Inverted Ranges, EOF boundaries.

## Execution
Run the test script from the scenario directory:
```bash
python test_ranges.py
```

## Findings
- **Bit-Perfect Slicing**: ✅ Extracted exactly the requested 11 lines in the happy path test.
- **EOF Resilience**: ✅ Gracefully handled requests extending past the end of the file by stopping at the final line.
- **Safety Fallbacks**: ✅ Correctly returned empty results for inverted or entirely out-of-bounds ranges without crashing the server.
