import calendar
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

from db import (
    add_list,
    add_task,
    complete_task,
    create_empty_list,
    delete_list,
    get_lists,
    get_scheduled_tasks,
    get_tasks_by_list,
    init_db,
    update_list_name,
)

app = Flask(__name__)


@app.route("/")
def index():
    init_db()
    lists = get_lists()
    current_list_id = int(request.args.get("list", 1))
    edit_list_id = int(request.args.get("edit", 0))
    tasks = get_tasks_by_list(current_list_id)
    scheduled = get_scheduled_tasks()
    pending = sum(1 for task in tasks if not task["done"])

    current_list_name = "Inbox"
    for lst in lists:
        if lst["id"] == current_list_id:
            current_list_name = lst["name"]
            break

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


@app.post("/tasks")
def create_task():
    title = (request.form.get("title") or "").strip()
    list_id = int(request.form.get("list_id", 1))
    due_date = request.form.get("due_date") or None
    if title:
        add_task(title, list_id, due_date)
    return redirect(url_for("index", list=list_id))


@app.post("/tasks/<int:task_id>/complete")
def mark_complete(task_id: int):
    complete_task(task_id)
    return redirect(url_for("index"))


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
