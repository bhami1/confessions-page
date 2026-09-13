"""
Database layer for the Whispers placeholder project.

SQLite is used for local development.
The Streamlit UI should call these functions instead of directly
writing SQL, which makes it easier to replace SQLite with MySQL later.
"""

import hashlib
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "whispers.db"
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS confessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                ip_hash TEXT,
                created_at TEXT NOT NULL
            )
        """)

        connection.commit()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str) -> bool:
    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (username, password_hash, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    username,
                    hash_password(password),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(username: str, password: str) -> bool:
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id FROM users
            WHERE username = ? AND password_hash = ?
            """,
            (username, hash_password(password)),
        ).fetchone()

    return user is not None


def hash_ip(ip_address: str) -> str:
    """
    Placeholder privacy-friendly IP handling.
    The actual IP is not stored; only a one-way hash is saved.
    """
    salt = os.getenv("IP_HASH_SALT", "development-placeholder-salt")
    return hashlib.sha256(
        f"{salt}:{ip_address}".encode("utf-8")
    ).hexdigest()


def add_confession(content: str, ip_address: str = "") -> bool:
    content = content.strip()

    if not content:
        return False

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO confessions (content, ip_hash, created_at)
            VALUES (?, ?, ?)
            """,
            (
                content,
                hash_ip(ip_address) if ip_address else None,
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            ),
        )
        connection.commit()

    return True


def get_confessions(limit: int = 50):
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


def seed_demo_data():
    """Insert a few safe placeholder records for development."""
    if get_confessions(limit=1):
        return

    demo = [
        "I am nervous about starting something completely new.",
        "Sometimes the smallest achievements feel the most satisfying.",
        "I want to become better at the things I enjoy.",
    ]

    for text in demo:
        add_confession(text)
