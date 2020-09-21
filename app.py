from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jplv123.YJ@localhost/test_sqlalchemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    def __init__(self, title, description):
        self.title = title
        self.description = description

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True) #--for many

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    new_task = Task(title,description)
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    results = tasks_schema.dump(all_tasks)

    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

if __name__ == "__main__":
    app.run(debug=True)