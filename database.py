import sqlite3
from datetime import datetime

DB_NAME = "visitor_log.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            face_encoding BLOB,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_visitor(name, face_encoding=None, image_path=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute('''
        INSERT INTO visitors (name, timestamp, face_encoding, image_path)
        VALUES (?, ?, ?, ?)
    ''', (name, timestamp, face_encoding, image_path))

    conn.commit()
    conn.close()
