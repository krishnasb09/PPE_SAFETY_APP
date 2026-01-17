from datetime import datetime
from database import get_connection

def evaluate_violation(person_id, missing_ppe_list):
    """
    Determines PPE compliance.
    Returns:
        is_compliant (bool)
        status (str)
    """
    if not missing_ppe_list:
        return True, "COMPLIANT"
    return False, "VIOLATION"


def log_violation(person_id, missing_ppe_list, video_time,
                  source="Unknown", status="VIOLATION"):
    """
    Logs ONLY violations to database.
    """
    if status != "VIOLATION":
        return  # Do NOT log compliant workers

    conn = get_connection()
    c = conn.cursor()

    now = datetime.now()
    missing_str = ", ".join(missing_ppe_list)

    try:
        c.execute("""
        INSERT INTO violations
        (person_id, missing_ppe, video_time, timestamp, date, source, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            person_id,
            missing_str,
            video_time,
            now.strftime("%Y-%m-%d %H:%M:%S"),
            now.strftime("%Y-%m-%d"),
            source,
            status
        ))
        conn.commit()
    except Exception as e:
        print("Violation logging error:", e)
    finally:
        conn.close()
