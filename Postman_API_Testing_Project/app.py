
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample task database
tasks = {
    1: {
        "id": 1,
        "title": "Complete mini project",
        "priority": "High",
        "status": "In Progress",
        "due_date": "2026-12-01"
    },
    2: {
        "id": 2,
        "title": "Prepare presentation",
        "priority": "Medium",
        "status": "To Do",
        "due_date": "2026-12-05"
    }
}

next_id = 3

PRIORITIES = ["Low", "Medium", "High"]
STATUSES = ["To Do", "In Progress", "Done"]


# Validate task details
def validate_task(data):

    if not isinstance(data, dict):
        return "A valid JSON object is required"

    title = data.get("title")

    if not isinstance(title, str):
        return "Title must be text"

    if len(title.strip()) < 3 or len(title.strip()) > 50:
        return "Title must contain 3 to 50 characters"

    if data.get("priority") not in PRIORITIES:
        return "Invalid priority"

    if data.get("status") not in STATUSES:
        return "Invalid status"

    due_date = data.get("due_date")

    if due_date is not None:
        if not isinstance(due_date, str):
            return "Invalid due date"

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return "Due date must be YYYY-MM-DD"

    return None


# 1. GET all tasks (supports status filtering)
@app.route('/tasks', methods=['GET'])
def get_tasks():

    status = request.args.get("status")

    if status and status not in STATUSES:
        return jsonify({"error": "Invalid status filter"}), 400

    result = list(tasks.values())

    if status:
        result = [
            task for task in result
            if task["status"] == status
        ]

    return jsonify(result), 200


# 2. GET task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):

    task = tasks.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


# 3. POST - Create task
@app.route('/tasks', methods=['POST'])
def create_task():

    global next_id

    data = request.get_json(silent=True)

    error = validate_task(data)

    if error:
        return jsonify({"error": error}), 400

    task = {
        "id": next_id,
        "title": data["title"].strip(),
        "priority": data["priority"],
        "status": data["status"],
        "due_date": data.get("due_date")
    }

    tasks[next_id] = task
    next_id += 1

    return jsonify(task), 201


# 4. PUT - Update task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True)

    error = validate_task(data)

    if error:
        return jsonify({"error": error}), 400

    tasks[task_id] = {
        "id": task_id,
        "title": data["title"].strip(),
        "priority": data["priority"],
        "status": data["status"],
        "due_date": data.get("due_date")
    }

    return jsonify(tasks[task_id]), 200


# 5. DELETE - Delete task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
