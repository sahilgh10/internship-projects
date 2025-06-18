# 🧰 Interior Project Task Tracker

A simple command-line task manager written in Python to help track tasks for interior design projects. Add, view, complete, and delete tasks all from one terminal interface — perfect for managing client-based work during an internship!

---

## 📦 Features

- ✅ Add new tasks under a project  
- 👀 View all tasks, or filter by pending/completed  
- ✔️ Mark tasks as completed  
- 🗑️ Delete tasks  
- 🌀 Runs in an interactive loop for continuous usage  

---

## 🧑‍💻 How to Use

### 1. Run the Script

```bash
python task_tracker.py
```

### 2. Choose from the Menu

You'll see:

```
📋 Interior Project Task Tracker  
1. Add Task  
2. View All Tasks  
3. View Pending Tasks  
4. View Completed Tasks  
5. Mark Task as Completed  
6. Delete Task  
7. Exit  
```

### 3. Add Task Example

- Project: `Modular Kitchen`  
- Task: `Finalize cabinet colors`  
- Deadline: `22 June`  

---

## 📁 Sample Output

```text
📋 Interior Project Task Tracker
1. Add Task
2. View All Tasks
3. View Pending Tasks
4. View Completed Tasks
5. Mark Task as Completed
6. Delete Task
7. Exit
Choose an option (1-7): 1

Enter project name: Bedroom
Enter task description: Select wardrobe design
Enter deadline (e.g., 15 June): 25 June
✅ Task added successfully!
```

---

## 📄 Code Structure

All functionality is handled within a single Python file using:

- `tasks = []` — in-memory task storage  
- `add_task()` — to create new tasks  
- `view_tasks()` — with optional filters  
- `mark_complete()` — to update status  
- `delete_task()` — to remove tasks  
- Main menu loop for interactivity  

---

## ⚠️ Limitations

- Tasks are stored **only in memory** — once you exit, all data is lost  
- No GUI — this is a **command-line** tool  

---

## 🚀 Future Improvements (Optional Ideas)

- Save tasks to a JSON or CSV file  
- Add due-date reminders  
- Sort by deadline  
- Add categories or priorities  
- Build a simple GUI using Tkinter  

---

## 🏷️ Author

**Sahil Gholap**  
Built as part of internship Python tools collection 🚀
