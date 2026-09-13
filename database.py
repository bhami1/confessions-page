import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).parent / "data" / "confessions.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the confessions table if it doesn't already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS confessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.commit()


def add_confession(content: str) -> bool:
    """Store a confession anonymously."""
    content = content.strip()

    if not content:
        return False

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO confessions (content, created_at)
            VALUES (?, ?)
            """,
            (
                content,
                datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M UTC"
                ),
            ),
        )

        connection.commit()

    return True


def get_confessions(limit: int = 50):
    """Retrieve the latest anonymous confessions."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, content, created_at
            FROM confessions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
