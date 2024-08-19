import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Task:
    def __init__(self, title, description, deadline, category="General"):
        self.title = title
        self.description = description
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.completed = False
        self.category = category

    def __repr__(self):
        status = "Выполнена" if self.completed else "Не выполнена"
        return f"{self.title} - {self.description} (до {self.deadline.date()}) [{self.category}] - {status}"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

    def get_all_tasks(self):
        return self.tasks

    def get_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category == category]

    def mark_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.task_manager = TaskManager()

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(pady=20)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, bd=2, relief="solid")
        self.task_listbox.pack(side=tk.LEFT, padx=20)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.add_task_button = tk.Button(self.root, text="Добавить задачу", command=self.add_task, bg="lightblue", width=20)
        self.add_task_button.pack(pady=5)

        self.complete_task_button = tk.Button(self.root, text="Завершить задачу", command=self.complete_task, bg="lightgreen", width=20)
        self.complete_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(self.root, text="Удалить задачу", command=self.delete_task, bg="lightcoral", width=20)
        self.delete_task_button.pack(pady=5)

        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_manager.get_all_tasks():
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Добавить задачу")
        add_task_window.geometry("300x200")

        tk.Label(add_task_window, text="Название:", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        title_entry = tk.Entry(add_task_window, width=30)
        title_entry.grid(row=0, column=1, pady=5)

        tk.Label(add_task_window, text="Описание:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        description_entry = tk.Entry(add_task_window, width=30)
        description_entry.grid(row=1, column=1, pady=5)

        tk.Label(add_task_window, text="Крайний срок (YYYY-MM-DD):", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        deadline_entry = tk.Entry(add_task_window, width=30)
        deadline_entry.grid(row=2, column=1, pady=5)

        tk.Label(add_task_window, text="Категория:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        category_entry = tk.Entry(add_task_window, width=30)
        category_entry.grid(row=3, column=1, pady=5)

        def save_task():
            title = title_entry.get()
            description = description_entry.get()
            deadline = deadline_entry.get()
            category = category_entry.get()

            try:
                task = Task(title, description, deadline, category)
                self.task_manager.add_task(task)
                self.update_task_listbox()
                add_task_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректная дата! Введите дату в формате YYYY-MM-DD.")

        tk.Button(add_task_window, text="Сохранить", command=save_task, bg="lightgreen", width=15).grid(row=4, columnspan=2, pady=10)

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.task_manager.mark_task_completed(task_index)
            self.update_task_listbox()

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.task_manager.delete_task(task_index)
            self.update_task_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


