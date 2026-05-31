"""flood_node.py — outputs 10MB of text to stress the pipe buffer."""
import sys
line = "FLOOD: " + "x" * 1000 + "\n"
for _ in range(10000):  # 10MB
    sys.stdout.write(line)
