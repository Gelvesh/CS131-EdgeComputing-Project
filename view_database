import sqlite3
import os

DB_FILE = 'visitor_log.db'

def view_image_rows_only():
    if not os.path.exists(DB_FILE):
        print(f"❌ Database file '{DB_FILE}' not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Find all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        try:
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            if "image_path" in column_names:
                print(f"\n📂 Table: {table_name} — Rows with image_path:")
                cursor.execute(f"SELECT * FROM {table_name} WHERE image_path IS NOT NULL")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("  (No rows with image_path)")
        except Exception as e:
            print(f"⚠️ Error accessing table {table_name}: {e}")

    conn.close()

if __name__ == '__main__':
    view_image_rows_only()
