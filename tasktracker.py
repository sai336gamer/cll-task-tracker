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
        tasks = []  

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

def listtasks(args):
    """List tasks, optionally filtering by status."""
    filter_status = args[0] if args else None  

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

        # Display tasks
        for task in tasks:
            print(f"ID: {task['id']}, Name: {task['name']}, Priority: {task['priority']}, Status: {task['status']}")

    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")


def update_task_progress(args):
    """Update only the progress/status of an existing task by ID"""
    task_id = args[0]
    new_status = args[1]

    # Load existing tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No tasks found.")
        return

    # Find task by ID and update only the status
    updated = False
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
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
    if len(args.args) > 1:
        print("Usage: python tasktracker.py list [status]")
    else:
        listtasks(args.args)  
elif args.command == "update":
    if len(args.args) != 2:
        print("Usage: python tasktracker.py update <task_id> <new_status>")
    else:
        update_task_progress(args.args)

