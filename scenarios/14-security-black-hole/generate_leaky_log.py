import random
import uuid

def generate_leaky_log(filename, count):
    # Fake patterns
    def fake_aws_key(): return f"AKIA{uuid.uuid4().hex[:16].upper()}"
    def fake_email(): return f"user_{random.randint(1,999)}@internal.corp"
    def fake_cc(): return "-".join([str(random.randint(1000, 9999)) for _ in range(4)])

    print(f"Generating {count} leaky log lines...")
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(count):
            secret_type = random.choice(["AWS", "EMAIL", "CC", "NONE"])
            msg = f"Event {i}: User session heartbeat."
            if secret_type == "AWS":
                msg = f"Event {i}: Auth failure for key {fake_aws_key()}."
            elif secret_type == "EMAIL":
                msg = f"Event {i}: Password reset sent to {fake_email()}."
            elif secret_type == "CC":
                msg = f"Event {i}: Payment processed for card {fake_cc()}."
            
            f.write(f"[2026-05-12 14:00] INFO: {msg}\n")
    print(f"Done. File '{filename}' created.")

if __name__ == "__main__":
    generate_leaky_log("leaky_secrets.log", 1500)
