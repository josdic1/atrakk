import sqlite3
import csv
import os

# Connect to the ACTUAL database (in instance folder)
conn = sqlite3.connect('instance/app.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Create exports folder
os.makedirs('exports', exist_ok=True)

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

# Export each table
for table in tables:
    print(f"Exporting {table}...")
    
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    if rows:
        # Get column names
        columns = rows[0].keys()
        
        # Write to CSV
        with open(f'exports/{table}.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows([dict(row) for row in rows])
        
        print(f"✓ {table}.csv created ({len(rows)} rows)")
    else:
        print(f"✗ {table} is empty")

conn.close()
print("\nAll tables exported to /exports folder!")