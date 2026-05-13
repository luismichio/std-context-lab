import json
import random

data = []
for i in range(100):
    data.append({
        "id": i,
        "uuid": f"user-{random.getrandbits(64):x}",
        "metadata": {
            "request_id": f"req-{i}",
            "internal_flags": ["ALPHA", "BETA", "INTERNAL_ONLY"],
            "debug_dump": "A" * 500  # Bloat
        },
        "payload": {
            "name": f"Item {i}",
            "value": random.random(),
            "status": random.choice(["ACTIVE", "INACTIVE", "PENDING"])
        },
        "links": [f"http://internal.api/v1/items/{i}"] * 5
    })

with open("massive_data.json", "w") as f:
    json.dump(data, f, indent=2)
