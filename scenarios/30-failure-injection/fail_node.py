"""fail_node.py — reads stdin, exits 1 with error message."""
import sys
sys.stdin.read()
sys.stderr.write("fail_node: deliberate failure\n")
sys.exit(1)
