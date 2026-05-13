import random
import os
from datetime import datetime, timedelta

def generate_giant_log(filename, target_size_mb):
    target_size_bytes = target_size_mb * 1024 * 1024
    levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    start_time = datetime.now()
    
    current_size = 0
    line_count = 0
    
    with open(filename, "w", encoding="utf-8") as f:
        while current_size < target_size_bytes:
            level = random.choice(levels)
            timestamp = (start_time + timedelta(seconds=line_count)).strftime("%Y-%m-%d %H:%M:%S")
            msg = f"Event {line_count}: Processing transaction {random.getrandbits(32):x}... Status OK."
            line = f"[{timestamp}] {level}: {msg}\n"
            f.write(line)
            current_size += len(line.encode('utf-8'))
            line_count += 1
            
            if line_count % 50000 == 0:
                print(f"Generated {current_size / (1024*1024):.1f} MB...")

    print(f"Final file '{filename}' size: {os.path.getsize(filename) / (1024*1024):.1f} MB ({line_count} lines).")

if __name__ == "__main__":
    generate_giant_log("giant_heart_attack.log", 50)
