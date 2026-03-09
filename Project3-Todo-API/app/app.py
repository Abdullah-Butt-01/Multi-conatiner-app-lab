from flask import Flask, request, jsonify
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/")
def home():
    return "Todo API Running"


@app.route("/task", methods=["POST"])
def add_task():
    task = request.json.get("task")

    task_id = r.incr("task_id")

    r.set(f"task:{task_id}", task)

    return jsonify({"id": task_id, "task": task})


@app.route("/tasks", methods=["GET"])
def get_tasks():

    tasks = []

    for key in r.keys("task:*"):
        tasks.append({
            "id": key.split(":")[1],
            "task": r.get(key)
        })

    return jsonify(tasks)


@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):

    r.delete(f"task:{id}")

    return jsonify({"message": "Task deleted"})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
