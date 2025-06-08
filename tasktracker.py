import argparse
import json
import random
import uuid
def addtask():
    
    id = str(uuid.uuid4())
    parser = argparse.ArgumentParser(description="Create a task project")

    
    parser.add_argument("name", type=str, help="Task Name")
    parser.add_argument("priority", type=str, choices=["low", "medium", "high"], help="Task Priority")
    parser.add_argument("status", type=str, choices=["todo", "inprogress", "done"], help="Task Status")

    args = parser.parse_args()

    task = {
        "id": id,
        "name": args.name,
        "priority": args.priority,
        "status": args.status

    }
    tasks= []
    tasks.append(task)
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
    print(f"Task added with ID: {id}")


def removetask():
    parser = argparse.ArgumentParser(description="Remove a task project")
    parser.add_argument("id", type=str, help="Task ID to remove")
    args = parser.parse_args()

    tasks = []
    with open("tasks.json", "r") as file:
        for line in file:
            task = json.loads(line.strip())
            if task["id"] != args.id:
                tasks.append(task)

    with open("tasks.json", "w") as file:
        for task in tasks:
            file.write(json.dumps(task) + "\n")

