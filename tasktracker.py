import argparse
import json
import random
def main():
    parser = argparse.ArgumentParser(description="Create a task project")

    parser.add_argument("id", type=int, help="Task ID")
    parser.add_argument("name", type=str, help="Task Name")
    parser.add_argument("priority", type=str, choices=["low", "medium", "high"], help="Task Priority")
    parser.add_argument("status", type=int, choices=["todo", "inprogress", "done"], help="Task Status")

    args = parser.parse_args()

    task = {
        "id": args.id,
        "name": args.name,
        "priority": args.priority,
        "status": args.status
    }