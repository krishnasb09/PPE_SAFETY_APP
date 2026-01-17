import sqlite3
from database import DB_NAME

def migrate_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        c.execute("ALTER TABLE violations ADD COLUMN source TEXT")
        print("Migrated 'violations' table: Added 'source' column.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("'source' column already exists.")
        else:
            print(f"Error migrating DB: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_db()
