import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    player TEXT,
    wins INTEGER
)
""")

conn.commit()
conn.close()
