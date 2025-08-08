import sqlite3

conn = sqlite3.connect('cms.db')
cursor = conn.cursor()

# Check if 'parent_id' column exists
cursor.execute("PRAGMA table_info(page);")
columns = [col[1] for col in cursor.fetchall()]

if 'parent_id' not in columns:
    cursor.execute("ALTER TABLE page ADD COLUMN parent_id INTEGER REFERENCES page(id);")
    print("Column 'parent_id' added to 'page' table.")
else:
    print("Column 'parent_id' already exists in 'page' table.")

conn.commit()
conn.close()
