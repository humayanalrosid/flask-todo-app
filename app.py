from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import  SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	note = db.Column(db.String(100))
	complete = db.Column(db.Boolean, default=False, nullable=False)

@app.route("/")
def index():
	todo_list = Todo.query.all()
	return render_template("todo.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
	title = request.form.get("title").capitalize()
	note = request.form.get("note").capitalize()
	new_todo = Todo(title=title, note=note, complete=False)
	db.session.add(new_todo)
	db.session.commit()
	return redirect(url_for("index"))

@app.route("/update/<int:task_id>")
def update(task_id):
	todo = Todo.query.filter_by(id=task_id).first()
	todo.complete = not todo.complete
	db.session.commit()
	return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
	todo = Todo.query.filter_by(id=task_id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for("index"))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)

