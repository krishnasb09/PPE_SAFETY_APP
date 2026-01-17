import sqlite3
from database import DB_NAME

def add_date_column():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE violations ADD COLUMN date TEXT")
        print("Added 'date' column.")
    except Exception as e:
        print(f"Error (maybe exists): {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_date_column()
