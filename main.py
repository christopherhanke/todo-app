from flask import Flask, render_template, request, redirect, url_for
from models import db, Todo

app = Flask(__name__)
db.create_all()


@app.route("/")
def index():
    # show all todos
    todo_list = db.query(Todo).all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return redirect(url_for("index"))

    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.add(new_todo)
    db.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.query(Todo).filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.query(Todo).filter_by(id=todo_id).first()
    db.delete(todo)
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
