import argparse
import json
import uuid
import os
from datetime import datetime

def addtask(args):
    """Add a new task to the task tracker."""
    if len(args) != 3:
        print("Usage: python tasktracker.py add <name> <priority> <status>")
        return

    id = str(uuid.uuid4())
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    task = {
        "id": id,
        "name": args[0],
        "priority": args[1],
        "status": args[2],
        "created_at": created_at,
        "updated_at": created_at  
    }

    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []  

    tasks.append(task)
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added with ID: {id} on {created_at}")

def removetask(args):
    """Remove a task by ID."""
    if len(args) != 1:
        print("Usage: python tasktracker.py remove <task_id>")
        return

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

def listtasks(args=None):
    """List tasks, optionally filtering by status, and show creation date."""
    filter_status = args[0] if args and len(args) > 0 else None  

    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        if not tasks:
            print("No tasks found.")
            return

        if filter_status:
            tasks = [task for task in tasks if task["status"] == filter_status]
            if not tasks:
                print(f"No tasks found with status '{filter_status}'.")
                return

        for task in tasks:
            # Ensure "updated_at" exists before accessing it
            updated_at = task.get("updated_at", "N/A")  
            print(f"ID: {task['id']}, Name: {task['name']}, Priority: {task['priority']}, Status: {task['status']}, Created: {task['created_at']}, Updated: {updated_at}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")


def update_task_progress(args):
    """Update only the progress/status of an existing task by ID"""
    if len(args) != 2:
        print("Usage: python tasktracker.py update <task_id> <new_status>")
        return

    task_id = args[0]
    new_status = args[1]

    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")
        return

    updated = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = True
            break  

    if not updated:
        print(f"No task found with ID {task_id}.")
        return

    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task {task_id} progress updated to '{new_status}'.")

parser = argparse.ArgumentParser(description="Task Tracker CLI")
parser.add_argument("command", choices=["add", "remove", "list", "update"], help="Task command")
parser.add_argument("args", nargs="*", help="Arguments for the selected command")

args = parser.parse_args()

if args.command == "add":
    addtask(args.args)  # Correctly passes argument list
elif args.command == "remove":
    removetask(args.args)
elif args.command == "list":
    listtasks(args.args)  
elif args.command == "update":
    update_task_progress(args.args)
