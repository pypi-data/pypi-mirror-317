#!/usr/bin/env python3

import sys
from .utils import *

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "hamburger":
        print("I love U 🍔")
        return
    
    if len(sys.argv) < 2:
        print("Usage: task_tracker <command> [options]")
        print("Commands:")
        print("add ""task name"" - Add a new task")
        print("update <task_id> ""new task name"" - Update a task")
        print("delete <task_id> - Delete a task")
        print("mark-done <task_id> - Mark a task as done")
        print("mark-onGoing <task_id> - Mark a task as on-going")
        print("mark-todo <task_id> - Mark a task as to do(default)")
        print("list - List all tasks")
        print("list done - List all done tasks")
        print("list not done - List all not done tasks")
        print("list on-going - List all on-going tasks")
        print("list <task_id> - List a specific task")
        return
    
    command = sys.argv[1]

    if command == "add":
        if(len(sys.argv) < 3):
            print("Usage: task-cli add ""task name""")
            return
        add_task(sys.argv[2])
    elif command == "update":
        if(len(sys.argv) < 4):
            print("Usage: task-cli update <task_id> ""new task name""")
            return
        update_task(sys.argv[2],sys.argv[3])
    elif command == "delete":
        if(len(sys.argv) < 3):
            print("Usage: task-cli delete <task_id>")
            return
        delete_task(sys.argv[2])
    elif command == "mark-done":
        if(len(sys.argv) < 3):
            print("Usage: task-cli mark-done <task_id>")
            return
        mark_done(sys.argv[2])
    elif command == "mark-onGoing":
        if(len(sys.argv) < 3):
            print("Usage: task-cli mark-onGoing <task_id>")
            return
        mark_onGoing(sys.argv[2])
    elif command == "mark-todo":
        if(len(sys.argv) < 3):
            print("Usage: task-cli mark-onGoing <task_id>")
            return
        mark_todo(sys.argv[2])
    elif command == "list":
        if len(sys.argv) == 2:
            print("list - List all tasks")
            list_tasks()
        elif sys.argv[2] == "todo":
            list_todo()
        elif sys.argv[2] == "done":
            list_done()
        elif sys.argv[2] == "on-going":
            list_onGoing()
        else:
            print("list - List all tasks")
            print("list done - List all done tasks")
            print("list not done - List all not done tasks")
            print("list on-going - List all on-going tasks")
            print("list <task_id> - List a specific task")
    else:   
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
