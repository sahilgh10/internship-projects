from datetime import datetime
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,  # XAMPP default MySQL port
    user="root",
    password="",  # Leave blank if no password
    database="task_manager"
)
cursor = db.cursor()

def add_task():
    print("\n-- Add a New Task --")
    project = input("Enter project name: ")
    desc = input("Enter task details: ")

    while True:
        deadline_input = input("Set deadline (DD-MM-YYYY): ")
        try:
            deadline = datetime.strptime(deadline_input, "%d-%m-%Y")
            if deadline <= datetime.now():
                print("Deadline must be a future date.")
            else:
                break
        except ValueError:
            print("Invalid format. Use DD-MM-YYYY.")

    while True:
        priority = input("Set priority (High/Medium/Low): ").capitalize()
        if priority in ['High', 'Medium', 'Low']:
            break
        print("Invalid input. Choose from High, Medium, or Low.")

    while True:
        category = input("Set category (Work/Personal): ").capitalize()
        if category in ['Work', 'Personal']:
            break
        print("Invalid input. Choose either Work or Personal.")

    query = """
    INSERT INTO tasks (project, description, deadline, status, created, priority, category)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        project, desc, deadline.strftime("%Y-%m-%d"),
        "Pending", datetime.now().strftime("%Y-%m-%d"),
        priority, category
    )
    cursor.execute(query, values)
    db.commit()
    print("✔ Task successfully added!\n")

def view_tasks(filter_status=None, order_by=None):
    query = "SELECT * FROM tasks"
    if filter_status:
        query += f" WHERE status = '{filter_status}'"
    if order_by:
        query += f" ORDER BY {order_by}"

    cursor.execute(query)
    result = cursor.fetchall()

    print("\n-- Task List --")
    if not result:
        print("No tasks found.\n")
        return

    for i, task in enumerate(result, 1):
        deadline_str = task[3].strftime('%d-%m-%Y') if task[3] else "N/A"
        created_str = task[5].strftime('%d-%m-%Y') if task[5] else "N/A"
        print(f"{i}) {task[1]} - {task[2]} [{created_str}]")
        print(f"   ➤ Deadline: {deadline_str} | Created: {created_str} | Priority: {task[6]} | Category: {task[7]}")
    print()

def complete_task():
    cursor.execute("SELECT * FROM tasks WHERE status = 'Pending'")
    tasks = cursor.fetchall()
    if not tasks:
        print("All tasks are already completed!\n")
        return
    view_tasks("Pending")
    try:
        choice = int(input("Enter task number to mark as complete: ")) - 1
        task_id = tasks[choice][0]
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = %s", (task_id,))
        db.commit()
        print("✔ Task marked as completed.\n")
    except:
        print("Invalid selection.\n")

def delete_task():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks to delete.\n")
        return
    view_tasks()
    try:
        choice = int(input("Choose task number to delete: ")) - 1
        task_id = tasks[choice][0]
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.commit()
        print("✔ Task deleted.\n")
    except:
        print("Invalid input.\n")

def edit_task():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks to edit.\n")
        return
    view_tasks()
    try:
        idx = int(input("Task number to edit: ")) - 1
        task = tasks[idx]
        task_id = task[0]

        new_project = input(f"New project name ({task[1]}): ") or task[1]
        new_desc = input(f"New description ({task[2]}): ") or task[2]

        cursor.execute("""
            UPDATE tasks SET project = %s, description = %s WHERE id = %s
        """, (new_project, new_desc, task_id))
        db.commit()
        print("✔ Task updated.\n")
    except:
        print("Invalid selection.\n")

def search_tasks():
    keyword = input("Enter exact project name or description to search: ")
    cursor.execute("""
        SELECT * FROM tasks WHERE project = %s OR description = %s
    """, (keyword, keyword))
    result = cursor.fetchall()

    print("\n-- Search Results --")
    if not result:
        print("No matching tasks found.\n")
        return

    for i, task in enumerate(result, 1):
        deadline_str = task[3].strftime('%d-%m-%Y') if task[3] else "N/A"
        created_str = task[5].strftime('%d-%m-%Y') if task[5] else "N/A"
        print(f"{i}) {task[1]} - {task[2]} [{created_str}]")
        print(f"   ➤ Deadline: {deadline_str} | Created: {created_str} | Priority: {task[6]} | Category: {task[7]}")
    print()

def sort_menu():
    print("\n-- Sort Tasks --")
    print("1. By Deadline")
    print("2. By Project Name")
    print("3. By Priority")
    choice = input("Choose option: ").strip()
    if choice == '1':
        view_tasks(order_by="deadline")
    elif choice == '2':
        view_tasks(order_by="project")
    elif choice == '3':
        view_tasks(order_by="FIELD(priority, 'High', 'Medium', 'Low')")
    else:
        print("Invalid choice.\n")

def main():
    while True:
        print("\n====== Task Manager (MySQL) ======")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. Mark Task as Completed")
        print("6. Delete Task")
        print("7. Edit Task")
        print("8. Search Tasks")
        print("9. Sort Tasks")
        print("10. Exit")
        print("=" * 35)

        choice = input("Choose option (1-10): ").strip()
        if choice == '1': add_task()
        elif choice == '2': view_tasks()
        elif choice == '3': view_tasks("Pending")
        elif choice == '4': view_tasks("Completed")
        elif choice == '5': complete_task()
        elif choice == '6': delete_task()
        elif choice == '7': edit_task()
        elif choice == '8': search_tasks()
        elif choice == '9': sort_menu()
        elif choice == '10':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid input. Try again.\n")

main()
