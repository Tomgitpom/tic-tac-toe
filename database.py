import sqlite3

DB_NAME = "database.db"


def init_db(db_name=DB_NAME):
    """Luo tietokannan ja scores-taulun, jos niitä ei vielä ole."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        player TEXT PRIMARY KEY,
        wins INTEGER
    )
    """)

    conn.commit()
    conn.close()


def get_player_wins(player, db_name=DB_NAME):
    """Hakee pelaajan voittojen määrän tietokannasta."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT wins FROM scores WHERE player = ?", (player,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    return 0


def save_win(player, db_name=DB_NAME):
    """Lisää pelaajalle yhden voiton tietokantaan."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT wins FROM scores WHERE player = ?", (player,))
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE scores SET wins = wins + 1 WHERE player = ?",
            (player,)
        )
    else:
        cursor.execute(
            "INSERT INTO scores (player, wins) VALUES (?, ?)",
            (player, 1)
        )

    conn.commit()
    conn.close()
