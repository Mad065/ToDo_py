import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "todo.db"

DEFAULT_LISTS = ["Inbox", "Hoy", "Programadas", "Registro"]


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                is_default INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                list_id INTEGER NOT NULL DEFAULT 1,
                due_date TEXT,
                FOREIGN KEY (list_id) REFERENCES lists (id)
            )
            """
        )
        for name in DEFAULT_LISTS:
            connection.execute(
                "INSERT OR IGNORE INTO lists (name, is_default) VALUES (?, 1)",
                (name,)
            )


def get_lists() -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, is_default FROM lists ORDER BY is_default DESC, id ASC"
        ).fetchall()
    return [
        {"id": row["id"], "name": row["name"], "is_default": bool(row["is_default"])}
        for row in rows
    ]


def add_list(name: str) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("INSERT INTO lists (name) VALUES (?)", (name,))


def get_tasks_by_list(list_id: int) -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, done, created_at, due_date FROM tasks WHERE list_id = ? ORDER BY done ASC, id DESC",
            (list_id,)
        ).fetchall()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
            "created_at": row["created_at"],
            "due_date": row["due_date"],
        }
        for row in rows
    ]


def get_scheduled_tasks() -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT t.id, t.title, t.due_date, l.name as list_name
            FROM tasks t
            JOIN lists l ON t.list_id = l.id
            WHERE t.due_date IS NOT NULL AND t.done = 0
            ORDER BY t.due_date ASC
            """
        ).fetchall()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "due_date": row["due_date"],
            "list_name": row["list_name"],
        }
        for row in rows
    ]


def add_task(title: str, list_id: int = 1, due_date: str | None = None) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO tasks (title, list_id, due_date) VALUES (?, ?, ?)",
            (title, list_id, due_date)
        )


def complete_task(task_id: int) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))


def create_empty_list() -> int:
    init_db()
    with get_connection() as connection:
        cursor = connection.execute("INSERT INTO lists (name) VALUES (?)", ("",))
        return cursor.lastrowid


def update_list_name(list_id: int, name: str) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute(
            "UPDATE lists SET name = ? WHERE id = ? AND is_default = 0",
            (name, list_id)
        )


def delete_list(list_id: int) -> None:
    init_db()
    with get_connection() as connection:
        connection.execute("DELETE FROM tasks WHERE list_id = ?", (list_id,))
        connection.execute(
            "DELETE FROM lists WHERE id = ? AND is_default = 0",
            (list_id,)
        )
