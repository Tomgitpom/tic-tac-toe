import sqlite3
from pathlib import Path

# Haetaan database.db samasta kansiosta, missä tämä show_scores.py tiedosto on.
DB_PATH = Path(__file__).resolve().parent / "database.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Varmistetaan, että scores-taulu on olemassa.
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    player TEXT PRIMARY KEY,
    wins INTEGER
)
""")

cursor.execute("SELECT player, wins FROM scores ORDER BY wins DESC")
rows = cursor.fetchall()

print("Tallennetut pisteet:")
print("-------------------")

if rows:
    for player, wins in rows:
        print(f"{player}: {wins}")
else:
    print("Ei tallennettuja pisteitä vielä.")

conn.close()