import sqlite3
from database import DB_NAME

def fix_schema():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    
    c.execute("PRAGMA table_info(violations)")
    columns = [row[1] for row in c.fetchall()]
    print(f"Current columns: {columns}")
    
    
    if "video_time" not in columns:
        try:
            c.execute("ALTER TABLE violations ADD COLUMN video_time TEXT")
            print("Added 'video_time' column.")
        except Exception as e:
            print(f"Error adding video_time: {e}")

    
    if "source" not in columns:
        try:
            c.execute("ALTER TABLE violations ADD COLUMN source TEXT")
            print("Added 'source' column.")
        except Exception as e:
            print(f"Error adding source: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_schema()
