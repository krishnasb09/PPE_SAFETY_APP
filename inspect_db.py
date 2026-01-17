import sqlite3
import pandas as pd
from database import DB_NAME

conn = sqlite3.connect(DB_NAME)
try:
    df = pd.read_sql("PRAGMA table_info(violations)", conn)
    print(df)
except Exception as e:
    print(e)
finally:
    conn.close()
