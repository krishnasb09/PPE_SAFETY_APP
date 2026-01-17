import sqlite3
import os
import auth
from database import get_connection, init_db
from violation_logic import log_violation

TEST_DB = "test_ppe_violations.db"

# Monkey patch database connection for testing
import database
original_get_connection = database.get_connection
database.DB_NAME = TEST_DB

def test_db_init():
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except PermissionError:
            pass # Ignore if we can't delete, might be new run
            
    init_db()
    assert os.path.exists(TEST_DB)
    print("DB Init: PASSED")

def test_auth():
    # Register
    success = auth.register_admin("testadmin", "password123")
    assert success == True
    print("Admin Register: PASSED")
    
    # Duplicate Register
    success = auth.register_admin("testadmin", "password123")
    assert success == False
    print("Duplicate Register check: PASSED")
    
    # Login Success
    assert auth.login_admin("testadmin", "password123") == True
    print("Login Success: PASSED")
    
    # Login Fail
    assert auth.login_admin("testadmin", "wrongpass") == False
    print("Login Fail: PASSED")

def test_violation_logging():
    # Log a violation
    log_violation(1, ["Helmet"], "00:00:05", "VIOLATION")
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM violations WHERE person_id=?", (1,))
    row = c.fetchone()
    conn.close()
    
    assert row is not None
    assert row["missing_ppe"] == "Helmet"
    assert row["video_time"] == "00:00:05"
    assert row["status"] == "VIOLATION"
    print("Violation Logging: PASSED")

if __name__ == "__main__":
    try:
        test_db_init()
        test_auth()
        test_violation_logging()
        print("\nALL TESTS PASSED")
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
    except Exception as e:
        print(f"\nERROR: {e}")
