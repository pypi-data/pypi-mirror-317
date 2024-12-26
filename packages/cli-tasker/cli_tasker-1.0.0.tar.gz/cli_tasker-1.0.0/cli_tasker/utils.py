import os
import json
import time
from tabulate import tabulate

TASK_FILE = "tasks.json"
table_header = ['ID', 'Task name', 'Status', 'Create time', 'Last update time']
def add_task(task_name):
    task = {
        "id": generate_task_id(),
        "name": task_name,
        "status": "todo",
        "created at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "last updated at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print(f"Task added successfully (ID: {task['id']}).")

def update_task(id, new_name):
    task_id = int(id)
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["name"] = new_name
            task["last updated at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) updated successfully.")
            return
    print(f"Task (ID: {task_id}) not found.")

def delete_task(args):
    task_id = int(args)
    tasks = load_tasks()
    if not any(task["id"] == task_id for task in tasks):
        print(f"Task (ID: {task_id}) not found.")
        return
    arrange = input("Do you want to re-arrange the task ID? (y/n): ").strip().lower()
    if arrange in ["yes", "y"]:
        tasks = [task for task in tasks if task["id"] != task_id]
        for i, task in enumerate(tasks):
            task["id"] = i + 1
        save_tasks(tasks)
        print(f"Task (ID: {task_id}) deleted successfully and task ID re-arranged.")
    else:
        tasks = [task for task in tasks if task["id"] != task_id]
        save_tasks(tasks)
        print(f"Task (ID: {task_id}) deleted successfully.")

def list_tasks():
    print("list all tasks:")
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    table = []
    for task in tasks:
        table.append(task.values())
    print(tabulate(table, headers=table_header, tablefmt="grid"))

def list_done():
    print("list tasks done:")
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    table = []
    for task in tasks:
        if task["status"] == "done":
            table.append(task.values())
    print(tabulate(table, headers=table_header, tablefmt="grid"))
    
def list_todo():
    print("list tasks to do:")
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    table = []
    for task in tasks:
        if task["status"] == "todo":
            table.append(task.values())
    print(tabulate(table, headers=table_header, tablefmt="grid"))
    
def list_onGoing():
    print("list tasks on-going:")
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    table = []
    for task in tasks:
        if task["status"] == "on-going":
            table.append(task.values())
    print(tabulate(table, headers=table_header, tablefmt="grid"))
            
def mark_todo(args):
    task_id = int(args)
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "todo"
            task["last updated at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) marked as to do.")
            return
    print(f"Task (ID: {task_id}) not found.")
    return
        
def mark_done(args):
    task_id = int(args)
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            print(f"Task (ID: {task_id}) marked as done.")
            delete_option = input(f"Do you want to delete Task (ID: {task_id})? (y/n): ").strip().lower()
            if delete_option in ["yes", "y"]:
                tasks.remove(task)
                save_tasks(tasks)
                print(f"Task (ID: {task_id}) has been deleted.")
            else:
                task["last updated at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"Task (ID: {task_id}) is still in the list.")
            save_tasks(tasks)
            return
            
    
    print(f"Task (ID: {task_id}) not found.")

def mark_onGoing(args):
    task_id = int(args)
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "on-going"
            task["last updated at"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            save_tasks(tasks)
            print(f"Task (ID: {task_id}) marked as on-going.")
            return
    print(f"Task (ID: {task_id}) not found.")
    return


def generate_task_id():
    tasks = load_tasks()
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)