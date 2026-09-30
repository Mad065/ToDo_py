import calendar
from datetime import date, timedelta

from flask import Flask, redirect, render_template, request, url_for

from db import (
    add_list,
    add_task,
    complete_task,
    create_empty_list,
    delete_list,
    delete_task,
    get_all_tasks,
    get_lists,
    get_scheduled_tasks,
    get_tasks_by_list,
    get_tasks_completed,
    get_tasks_scheduled,
    get_tasks_today,
    init_db,
    update_list_name,
    update_task,
)

app = Flask(__name__)


@app.route("/")
def index():
    init_db()
    lists = get_lists()
    current_list_id = int(request.args.get("list", 1))
    edit_list_id = int(request.args.get("edit", 0))

    current_list_name = "Inbox"
    for lst in lists:
        if lst["id"] == current_list_id:
            current_list_name = lst["name"]
            break

    if current_list_name == "Inbox":
        tasks = get_all_tasks()
    elif current_list_name == "Hoy":
        tasks = get_tasks_today()
    elif current_list_name == "Programadas":
        tasks = get_tasks_scheduled()
    elif current_list_name == "Registro":
        tasks = get_tasks_completed()
    else:
        tasks = get_tasks_by_list(current_list_id)

    scheduled = get_scheduled_tasks()
    pending = sum(1 for task in tasks if not task["done"])

    today = date.today()
    cal_days = calendar.Calendar().monthdayscalendar(today.year, today.month)

    return render_template(
        "index.html",
        lists=lists,
        current_list_id=current_list_id,
        current_list_name=current_list_name,
        edit_list_id=edit_list_id,
        tasks=tasks,
        scheduled=scheduled,
        pending=pending,
        cal_days=cal_days,
        today=today,
        month_name=calendar.month_name[today.month],
    )


@app.route("/calendar")
def calendar_view():
    today = date.today()
    year = int(request.args.get("year", today.year))
    month = int(request.args.get("month", today.month))
    week_offset = int(request.args.get("week", 0))

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    cal_days = calendar.Calendar().monthdayscalendar(year, month)
    scheduled = get_scheduled_tasks()

    tasks_by_date = {}
    for task in scheduled:
        d = task["due_date"]
        tasks_by_date.setdefault(d, []).append(task)

    # Calculate week navigation
    first_day = date(year, month, 1)
    current_week_start = first_day + timedelta(weeks=week_offset)
    current_week_start = current_week_start - timedelta(days=current_week_start.weekday())
    current_week_end = current_week_start + timedelta(days=6)

    prev_week = week_offset - 1
    next_week = week_offset + 1

    # Get tasks for current week
    week_tasks = []
    for task in scheduled:
        task_date = date.fromisoformat(task["due_date"])
        if current_week_start <= task_date <= current_week_end:
            week_tasks.append(task)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template(
        "calendar.html",
        cal_days=cal_days,
        today=today,
        year=year,
        month=month,
        month_name=calendar.month_name[month],
        scheduled=scheduled,
        tasks_by_date=tasks_by_date,
        prev_year=prev_year,
        prev_month=prev_month,
        next_year=next_year,
        next_month=next_month,
        week_offset=week_offset,
        prev_week=prev_week,
        next_week=next_week,
        week_start=current_week_start,
        week_end=current_week_end,
        week_tasks=week_tasks,
    )


@app.post("/tasks")
def create_task():
    title = (request.form.get("title") or "").strip()
    list_id = int(request.form.get("list_id", 1))
    due_date = request.form.get("due_date") or None
    from_calendar = request.form.get("from_calendar") == "1"
    if title:
        add_task(title, list_id, due_date)
    if from_calendar:
        return redirect(url_for("calendar_view"))
    return redirect(url_for("index", list=list_id))


@app.post("/tasks/<int:task_id>/complete")
def mark_complete(task_id: int):
    complete_task(task_id)
    list_id = int(request.args.get("list", 1))
    return redirect(url_for("index", list=list_id))


@app.post("/tasks/<int:task_id>/delete")
def delete_task_route(task_id: int):
    delete_task(task_id)
    list_id = int(request.args.get("list", 1))
    return redirect(url_for("index", list=list_id))


@app.post("/tasks/<int:task_id>/edit")
def edit_task(task_id: int):
    title = (request.form.get("title") or "").strip()
    due_date = request.form.get("due_date") or None
    if title:
        update_task(task_id, title, due_date)
    list_id = int(request.args.get("list", 1))
    return redirect(url_for("index", list=list_id))


@app.post("/lists")
def create_list():
    name = (request.form.get("name") or "").strip()
    if name:
        add_list(name)
    return redirect(url_for("index"))


@app.post("/lists/quick")
def quick_create_list():
    list_id = create_empty_list()
    return redirect(url_for("index", list=list_id, edit=list_id))


@app.post("/lists/<int:list_id>/rename")
def rename_list(list_id: int):
    name = (request.form.get("name") or "").strip()
    if name:
        update_list_name(list_id, name)
        return redirect(url_for("index", list=list_id))
    delete_list(list_id)
    return redirect(url_for("index"))


@app.post("/lists/<int:list_id>/delete")
def delete_list_route(list_id: int):
    delete_list(list_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
