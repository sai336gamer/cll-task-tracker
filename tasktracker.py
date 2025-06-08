import argparse
import json
import uuid
import os

def addtask(args):
    """Add a new task to the task tracker."""
    id = str(uuid.uuid4())

    task = {
        "id": id,
        "name": args[0],
        "priority": args[1],
        "status": args[2]
    }

    # Load existing tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []  # Handle missing/corrupt file

    tasks.append(task)
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added with ID: {id}")

def removetask(args):
    """Remove a task by ID."""
    task_id = args[0]

    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")
        return

    tasks = [task for task in tasks if task["id"] != task_id]

    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task with ID {task_id} removed successfully.")

def listtasks():
    """List all tasks."""
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(f"ID: {task['id']}, Name: {task['name']}, Priority: {task['priority']}, Status: {task['status']}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")

### **🔹 Simple Command Parsing Without Subparsers**

parser = argparse.ArgumentParser(description="Task Tracker CLI")
parser.add_argument("command", choices=["add", "remove", "list"], help="Task command")
parser.add_argument("args", nargs="*", help="Arguments for the selected command")

args = parser.parse_args()

if args.command == "add":
    if len(args.args) != 3:
        print("Usage: python tasktracker.py add <name> <priority> <status>")
    else:
        addtask(args.args)
elif args.command == "remove":
    if len(args.args) != 1:
        print("Usage: python tasktracker.py remove <task_id>")
    else:
        removetask(args.args)
elif args.command == "list":
    listtasks()
