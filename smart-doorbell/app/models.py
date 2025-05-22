import sqlite3
from datetime import datetime

DB_PATH = 'visitors.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS visitors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  timestamp DATETIME,
                  face_encoding BLOB,
                  image_path TEXT)''')
    conn.commit()
    conn.close()

def log_visitor(name, encoding, image_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO visitors 
                 (name, timestamp, face_encoding, image_path) 
                 VALUES (?, ?, ?, ?)''',
              (name, datetime.now(), sqlite3.Binary(encoding), image_path))
    conn.commit()
    conn.close()