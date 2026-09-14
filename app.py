from flask import Flask, redirect, render_template, request, url_for

from db import add_task, complete_task, init_db, list_tasks

app = Flask(__name__)


@app.route("/")
def index():
    tasks = list_tasks()
    pending = sum(1 for task in tasks if not task["done"])
    return render_template("index.html", tasks=tasks, pending=pending)


@app.post("/tasks")
def create_task():
    title = (request.form.get("title") or "").strip()
    if title:
        add_task(title)
    return redirect(url_for("index"))


@app.post("/tasks/<int:task_id>/complete")
def mark_complete(task_id: int):
    complete_task(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
