import random

def generate_apache_log(filename, count):
    print(f"Generating {count} apache log lines...")
    ips = [f"192.168.1.{i}" for i in range(1, 20)]
    bad_ips = ["192.168.1.5", "192.168.1.12", "192.168.1.19"]
    
    with open(filename, "w", encoding="utf-8") as f:
        for _ in range(count):
            ip = random.choice(ips)
            status = 200
            if ip == "192.168.1.5" and random.random() < 0.3: status = "CRITICAL"
            elif ip == "192.168.1.12" and random.random() < 0.2: status = "CRITICAL"
            elif ip == "192.168.1.19" and random.random() < 0.1: status = "CRITICAL"
            elif random.random() < 0.01: status = "CRITICAL"
            
            f.write(f"{ip} - - [13/May/2026:14:22:00 +0000] \"GET /api/data HTTP/1.1\" {status} 1024\n")
            
    print("Done.")

if __name__ == "__main__":
    generate_apache_log("apache_massive.log", 200000)
