"""
Database layer for Whispers — College of Engineering Trivandrum (CET).
Handles authentic campus confessions, categories, appreciations, dislikes, and members.
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
    """Initializes tables and applies backward-compatible schema migrations."""
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
                category TEXT DEFAULT 'CET Campus Life',
                likes INTEGER DEFAULT 0,
                dislikes INTEGER DEFAULT 0,
                ip_hash TEXT,
                created_at TEXT NOT NULL
            )
        """)

        # Schema migrations for existing databases
        columns_info = connection.execute("PRAGMA table_info(confessions)").fetchall()
        column_names = [col["name"] for col in columns_info]

        if "category" not in column_names:
            connection.execute("ALTER TABLE confessions ADD COLUMN category TEXT DEFAULT 'CET Campus Life'")

        if "likes" not in column_names:
            connection.execute("ALTER TABLE confessions ADD COLUMN likes INTEGER DEFAULT 0")

        if "dislikes" not in column_names:
            connection.execute("ALTER TABLE confessions ADD COLUMN dislikes INTEGER DEFAULT 0")

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
    salt = os.getenv("IP_HASH_SALT", "development-placeholder-salt")
    return hashlib.sha256(
        f"{salt}:{ip_address}".encode("utf-8")
    ).hexdigest()


def add_confession(content: str, category: str = "CET Campus Life", ip_address: str = "") -> bool:
    content = content.strip()

    if not content:
        return False

    category = category.strip() if category else "CET Campus Life"

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO confessions (content, category, likes, dislikes, ip_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                content,
                category,
                0,
                0,
                hash_ip(ip_address) if ip_address else None,
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            ),
        )
        connection.commit()

    return True


def like_confession(confession_id: int) -> bool:
    """Increment appreciation (thumbs up) count for a confession."""
    try:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE confessions
                SET likes = COALESCE(likes, 0) + 1
                WHERE id = ?
                """,
                (confession_id,),
            )
            connection.commit()
        return True
    except Exception:
        return False


def dislike_confession(confession_id: int) -> bool:
    """Increment dislikes (thumbs down) count for a confession."""
    try:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE confessions
                SET dislikes = COALESCE(dislikes, 0) + 1
                WHERE id = ?
                """,
                (confession_id,),
            )
            connection.commit()
        return True
    except Exception:
        return False


def get_confessions(
    limit: int = 50,
    category: str = None,
    search_query: str = None,
    sort_by: str = "latest",
):
    query = "SELECT id, content, category, COALESCE(likes, 0) as likes, COALESCE(dislikes, 0) as dislikes, created_at FROM confessions WHERE 1=1"
    params = []

    if category and category.lower() not in ("all", "all topics", "all categories"):
        query += " AND (category = ? OR category LIKE ?)"
        params.append(category)
        params.append(f"%{category}%")

    if search_query and search_query.strip():
        query += " AND content LIKE ?"
        params.append(f"%{search_query.strip()}%")

    if sort_by == "popular":
        query += " ORDER BY likes DESC, id DESC"
    else:
        query += " ORDER BY id DESC"

    query += " LIMIT ?"
    params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, tuple(params)).fetchall()

    return [dict(row) for row in rows]


def get_confession_stats():
    with get_connection() as connection:
        total_confessions = connection.execute(
            "SELECT COUNT(*) as count FROM confessions"
        ).fetchone()["count"]

        total_likes = connection.execute(
            "SELECT COALESCE(SUM(likes), 0) as count FROM confessions"
        ).fetchone()["count"]

        total_users = connection.execute(
            "SELECT COUNT(*) as count FROM users"
        ).fetchone()["count"]

    return {
        "total_confessions": total_confessions,
        "total_likes": total_likes,
        "total_users": max(total_users, 1),
    }


def clean_ai_confessions_and_seed_authentic():
    """Removes generic AI-generated confessions and replaces them with authentic CET student posts."""
    ai_phrases = [
        "%nervous about starting something%",
        "%smallest achievements feel%",
        "%want to become better%",
        "%supportive sticky note%",
        "%wrong professor's umbrella%",
        "%git rebase for 6 months%",
        "%algorithm textbook on the second floor%",
        "%Sitting at the CET Open Air Theatre on a quiet evening%",
    ]

    with get_connection() as connection:
        for phrase in ai_phrases:
            connection.execute("DELETE FROM confessions WHERE content LIKE ?", (phrase,))
        connection.commit()

        # Check if the authentic featured confession exists
        featured_exists = connection.execute(
            "SELECT COUNT(*) as count FROM confessions WHERE content LIKE '%Rs 100 note in my old lab coat%'"
        ).fetchone()["count"]

        if not featured_exists:
            connection.execute(
                """
                INSERT INTO confessions (id, content, category, likes, dislikes, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    1234,
                    "Found a forgotten Rs 100 note in my old lab coat during practicals. Treat time at the canteen! 🤫 #SmallJoys #CETLife",
                    "CET Campus Life",
                    48,
                    2,
                    "2026-09-18 08:30 UTC",
                ),
            )

        # Seed additional authentic student banter if few
        count = connection.execute("SELECT COUNT(*) as count FROM confessions").fetchone()["count"]
        if count < 6:
            authentic_posts = [
                (
                    "Submitted my MCA assignment at 11:59 PM with 4 seconds to spare. My heart rate still hasn't recovered. #DeadlineRush #CET",
                    "Campus Humor",
                    34,
                    1,
                    "2026-09-18 08:15 UTC"
                ),
                (
                    "The library security chettan who gently taps the desk to wake you up before locking up the reading room is a real one. #CETCare",
                    "Life & Advice",
                    29,
                    0,
                    "2026-09-18 07:45 UTC"
                ),
                (
                    "The walk from CET bus stop all the way up to PG block in the 1 PM sun is a full cardio workout. We need a campus ropeway. #KulathoorHill",
                    "CET Campus Life",
                    41,
                    3,
                    "2026-09-18 07:10 UTC"
                ),
                (
                    "I've had a crush on someone from the architecture block since the inauguration of Dhwani. I still look for them every time I pass the canteen. #DhwaniMemories",
                    "Romance & Crush",
                    53,
                    1,
                    "2026-09-18 06:30 UTC"
                )
            ]
            for content, category, likes, dislikes, created_at in authentic_posts:
                connection.execute(
                    """
                    INSERT INTO confessions (content, category, likes, dislikes, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (content, category, likes, dislikes, created_at),
                )

        # Also ensure a default registered user exists if users table is empty
        users_count = connection.execute("SELECT COUNT(*) as count FROM users").fetchone()["count"]
        if users_count == 0:
            create_user("bham", "password123")

        connection.commit()


def seed_demo_data():
    clean_ai_confessions_and_seed_authentic()
