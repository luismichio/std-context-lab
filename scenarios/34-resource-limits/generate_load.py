"""generate_load.py — generates large text input for resource stress testing.
Usage: python generate_load.py <size_mb>
"""
import sys

size_mb = float(sys.argv[1]) if len(sys.argv) > 1 else 100
target = int(size_mb * 1024 * 1024)
line = "STRESS: " + "log entry with some content " * 5 + "\n"
written = 0
while written < target:
    sys.stdout.write(line)
    written += len(line)
