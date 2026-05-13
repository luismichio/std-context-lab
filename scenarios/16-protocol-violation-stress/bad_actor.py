import sys
import os

def main():
    # Write some normal text
    sys.stdout.buffer.write(b"Here is some normal text.\n")
    
    # Write invalid utf-8 sequences
    sys.stdout.buffer.write(b"And here is some garbage: \xff\xfe\xfd\n")
    
    # Write some binary zeros
    sys.stdout.buffer.write(b"Binary \x00\x00\x00 data.\n")

if __name__ == "__main__":
    main()
