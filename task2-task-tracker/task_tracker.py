tasks = []

def add_task():
    project = input("Enter project name: ")
    task = input("Enter task description: ")
    deadline = input("Enter deadline (e.g., 15 June): ")
    tasks.append({
        "project": project,
        "task": task,
        "deadline": deadline,
        "status": "Pending"
    })
    print("✅ Task added successfully!\n")

def view_tasks(status_filter=None):
    if not tasks:
        print("No tasks available.\n")
        return

    for i, task in enumerate(tasks):
        if status_filter and task['status'] != status_filter:
            continue
        print(f"{i + 1}. [{task['status']}] {task['project']} - {task['task']} (Deadline: {task['deadline']})")
    print()

def mark_complete():
    view_tasks("Pending")
    task_num = int(input("Enter task number to mark complete: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks[task_num]['status'] = "Completed"
        print("✅ Task marked as completed!\n")
    else:
        print("❌ Invalid task number.\n")

def delete_task():
    view_tasks()
    task_num = int(input("Enter task number to delete: ")) - 1
    if 0 <= task_num < len(tasks):
        deleted = tasks.pop(task_num)
        print(f"🗑️ Deleted: {deleted['task']} from {deleted['project']}\n")
    else:
        print("❌ Invalid task number.\n")

# Main loop
while True:
    print("📋 Interior Project Task Tracker")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Completed")
    print("6. Delete Task")
    print("7. Exit")

    choice = input("Choose an option (1-7): ")

    if choice == '1':
        add_task()
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        view_tasks("Pending")
    elif choice == '4':
        view_tasks("Completed")
    elif choice == '5':
        mark_complete()
    elif choice == '6':
        delete_task()
    elif choice == '7':
        print("Exiting Task Tracker. Goodbye!")
        break
    else:
        print("❌ Invalid choice. Please try again.\n")
