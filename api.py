from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)


class TODORepo(object):
    TODOS = [
        {'task': 'learn English', "id": 1, "username": "zhangshan"},
        {'task': 'do sports', "id": 2, "username": "lisi"},
        {'task': 'learn English', "id": 3, "username": "wangwu"},
    ]

    def all(self):
        return self.TODOS

    def retrieve(self, field, value):
        for item in self.TODOS:
            if item.get(field) == value:
                return item

    def create(self, form):
        item = {
            "task": form.get("task"),
            "username": form.get("username")
        }
        self.TODOS.append(item)
        return item


class Todo(Resource):
    def get(self, todo_id):
        return TODORepo().retrieve("id", todo_id)


class TodoList(Resource):
    def get(self):
        return TODORepo().all()

    def post(self):
        form = self.get_form_data()
        data = TODORepo().create(form)
        return data, 200

    def get_form_data(self):
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str)
        parser.add_argument("user", type=str)
        return parser.parse_args()


api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
