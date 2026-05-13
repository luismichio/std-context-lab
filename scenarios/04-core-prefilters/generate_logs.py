import random
from datetime import datetime, timedelta

levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
start_time = datetime.now()

with open("noisy_app.log", "w") as f:
    for i in range(5000):
        level = random.choices(levels, weights=[70, 20, 7, 2, 1])[0]
        timestamp = (start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Event {i}: Processing request chunk {random.randint(100, 999)}..."
        if level == "CRITICAL":
            msg = f"Event {i}: FATAL SYSTEM FAILURE - Database connection lost at pool_id={random.randint(1, 10)}"
        
        f.write(f"[{timestamp}] {level}: {msg}\n")
