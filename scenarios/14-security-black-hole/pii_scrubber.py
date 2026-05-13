import sys
import re

def scrub_pii(text):
    # 1. AWS Keys
    text = re.sub(r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_KEY]", text)
    # 2. Emails
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]", text)
    # 3. Credit Cards
    text = re.sub(r"\b(?:\d{4}-){3}\d{4}\b", "[REDACTED_CC]", text)
    return text

if __name__ == "__main__":
    raw_input = sys.stdin.read()
    if raw_input:
        sys.stdout.write(scrub_pii(raw_input))
