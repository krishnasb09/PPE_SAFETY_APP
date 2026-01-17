import hashlib
import sqlite3
from database import get_connection

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verifies a stored password against a provided password."""
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

def register_admin(username, password):
    """Registers a new admin. Returns True if successful, False if username exists."""
    conn = get_connection()
    c = conn.cursor()
    
    hashed_pw = hash_password(password)
    
    try:
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    finally:
        conn.close()
        
    return success

def login_admin(username, password):
    """Authenticates an admin. Returns True if successful."""
    conn = get_connection()
    c = conn.cursor()
    
    hashed_pw = hash_password(password)
    
    c.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, hashed_pw))
    user = c.fetchone()
    
    conn.close()
    return user is not None
