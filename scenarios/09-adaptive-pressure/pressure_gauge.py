import os
import sys

def main():
    # 1. Read input data
    data = sys.stdin.read()
    
    # 2. Detect pressure from environment
    # In a real IDE, this might be set by the client based on token count.
    pressure = os.environ.get("CONTEXT_PRESSURE", "LOW").upper()
    
    # 3. Output a header with the signal
    if pressure == "HIGH":
        print(f"[SIGNAL: PRESSURE_HIGH] {data}")
    else:
        print(f"[SIGNAL: PRESSURE_LOW] {data}")

if __name__ == "__main__":
    main()
