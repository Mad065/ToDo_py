import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "todo.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def list_tasks() -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, done, created_at FROM tasks ORDER BY done ASC, id DESC"
        ).fetchall()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def add_task(title: str) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))


def complete_task(task_id: int) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
