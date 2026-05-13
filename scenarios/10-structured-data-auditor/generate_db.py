import sqlite3
import random
import uuid

def generate_mock_db():
    conn = sqlite3.connect('mock_telemetry.db')
    cursor = conn.cursor()
    
    # 1. Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_events (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            event_type TEXT,
            payload TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Insert 1000 rows of "noise"
    event_types = ["CLICK", "SCROLL", "HOVER", "RESIZE", "DRAG"]
    
    rows = []
    for i in range(1000):
        rows.append((
            str(uuid.uuid4()),
            random.choice(event_types),
            "A" * 500, # Bloated payload
        ))
    
    cursor.executemany('INSERT INTO user_events (user_id, event_type, payload) VALUES (?, ?, ?)', rows)
    
    conn.commit()
    conn.close()
    print("Mock database 'mock_telemetry.db' generated with 1000 rows.")

if __name__ == "__main__":
    generate_mock_db()
