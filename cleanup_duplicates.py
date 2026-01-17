"""
Database Cleanup Script
Removes duplicate violation logs, keeping only 1 entry per person per video source.
"""

import sqlite3
from database import get_connection
import os

def cleanup_duplicate_violations():
    """Remove duplicate logs for same person in same video"""
    print("\n" + "="*60)
    print("DATABASE CLEANUP - Removing Duplicate Violations")
    print("="*60)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT COUNT(*) FROM violations")
        before_count = cursor.fetchone()[0]
        print(f"\n📊 Total violations before cleanup: {before_count}")
        
       
        cursor.execute("SELECT COUNT(DISTINCT person_id) FROM violations")
        unique_persons = cursor.fetchone()[0]
        print(f"👥 Unique persons: {unique_persons}")
        
        
        cursor.execute("""
            SELECT person_id, source, COUNT(*) as count
            FROM violations
            GROUP BY person_id, source
            HAVING count > 1
            ORDER BY count DESC
        """)
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} person-video combinations with duplicates:")
            for person_id, source, count in duplicates[:10]:  # Show top 10
                print(f"   Person {person_id} in '{source}': {count} entries")
            if len(duplicates) > 10:
                print(f"   ... and {len(duplicates) - 10} more")
        
        
        print("\n🔧 Removing duplicates...")
        cursor.execute("""
            DELETE FROM violations
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM violations
                GROUP BY person_id, source
            )
        """)
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        
        cursor.execute("SELECT COUNT(*) FROM violations")
        after_count = cursor.fetchone()[0]
        
        print(f"\n✅ Cleanup complete!")
        print(f"   Removed: {deleted_count} duplicate entries")
        print(f"   Before: {before_count} entries")
        print(f"   After: {after_count} entries")
        print(f"   Unique persons: {unique_persons}")
        
        
        cursor.execute("""
            SELECT source, COUNT(DISTINCT person_id) as unique_persons, COUNT(*) as entries
            FROM violations
            GROUP BY source
        """)
        summary = cursor.fetchall()
        
        print(f"\n📋 Summary by source:")
        for source, persons, entries in summary:
            print(f"   {source}: {persons} persons, {entries} entries")
        
        return deleted_count
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

def backup_database():
    """Create a backup before cleanup"""
    import shutil
    from datetime import datetime
    
    db_path = "ppe_violations.db"
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"ppe_violations_backup_{timestamp}.db"
        shutil.copy2(db_path, backup_path)
        print(f"💾 Backup created: {backup_path}")
        return backup_path
    return None

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("PPE VIOLATIONS DATABASE CLEANUP")
    print("#"*60)
    
    
    backup_path = backup_database()
    
    
    deleted = cleanup_duplicate_violations()
    
    print("\n" + "="*60)
    if deleted > 0:
        print(f"✅ Successfully cleaned {deleted} duplicate entries!")
        if backup_path:
            print(f"💾 Original database backed up to: {backup_path}")
    else:
        print("✅ No duplicates found or cleanup skipped")
    print("="*60)
    print("\n🔄 Refresh your dashboard to see the cleaned data!\n")
