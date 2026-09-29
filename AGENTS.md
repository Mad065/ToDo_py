# AGENTS.md

## Run

```bash
python app.py
```

App runs at http://127.0.0.1:5000 with debug mode enabled.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Architecture

- `app.py` — Flask routes and controller logic (all routes defined here)
- `db.py` — SQLite layer; `init_db()` auto-creates tables and seeds default lists on first call
- `templates/` — Jinja2 templates (`index.html`, `calendar.html`)
- `static/style.css` — single stylesheet with CSS custom properties for theming

## Database

- SQLite file: `todo.db` (auto-generated, gitignored)
- Tables: `lists` (id, name, is_default) and `tasks` (id, title, done, created_at, list_id, due_date)
- Default lists seeded on init: Inbox, Hoy, Programadas, Registro
- No migrations — schema changes require manual table recreation

## Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Main view with lists, tasks, calendar widget |
| GET | `/calendar` | Full calendar page with month navigation (`?year=&month=`) |
| POST | `/tasks` | Create task (title, list_id, due_date) |
| POST | `/tasks/<id>/complete` | Mark task done |
| POST | `/lists` | Create named list |
| POST | `/lists/quick` | Create empty list |
| POST | `/lists/<id>/rename` | Rename list (empty name deletes it) |
| POST | `/lists/<id>/delete` | Delete custom list and its tasks |

## Conventions

- No tests, lint, or typecheck configured
- UI text is in Spanish
- Theme system uses CSS variables + localStorage (6 gradient themes, blur intensity, animation toggle)
- Glassmorphism design: `backdrop-filter: blur()` on glass panels, semi-transparent backgrounds
