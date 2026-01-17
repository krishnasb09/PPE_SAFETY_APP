import sqlite3
import os

DB_NAME = "ppe_violations.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """Initializes the database with necessary tables."""
    conn = get_connection()
    c = conn.cursor()

   
    c.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    
    c.execute("""
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        missing_ppe TEXT,
        video_time TEXT,
        timestamp TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database {DB_NAME} initialized successfully.")
