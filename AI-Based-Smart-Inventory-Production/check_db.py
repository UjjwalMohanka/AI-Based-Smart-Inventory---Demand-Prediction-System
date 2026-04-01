import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'app', 'production.db')
print(f"Checking database at: {db_path}")

if not os.path.exists(db_path):
    print("Database not found!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n--- Predictions Table ---")
    try:
        cursor.execute("SELECT * FROM prediction LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            # Check types
            for i, val in enumerate(row):
                print(f"  Col {i}: {type(val)} - {val}")
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n--- Sales Table ---")
    try:
        cursor.execute("SELECT * FROM sales LIMIT 5")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
        
    conn.close()
