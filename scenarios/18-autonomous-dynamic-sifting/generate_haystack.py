import random

def generate_haystack(filename, count):
    print(f"Generating {count} log lines...")
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(count):
            if i == count // 2:
                f.write(f"[2026-05-13 14:22] CRITICAL: FATAL_ERROR_CODE_9942 - Database connection completely dropped by peer at pool_id=14.\n")
            else:
                f.write(f"[2026-05-13 14:22] INFO: Event {i}: Standard system heartbeat. All ok.\n")
    print("Done.")

if __name__ == "__main__":
    generate_haystack("needle_in_haystack.log", 150000)
