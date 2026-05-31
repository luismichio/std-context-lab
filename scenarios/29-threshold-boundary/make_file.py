"""make_file.py — creates a file with exactly N bytes of content.
Usage: python make_file.py <path> <size_bytes>
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
size = int(sys.argv[2])
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(b"X" * size)
print(f"Created {path} ({size} bytes)")
