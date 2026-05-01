import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"text": "Прочитать статью по Python", "type": "учёба"},
    {"text": "Сделать зарядку 15 минут", "type": "спорт"},
    {"text": "Ответить на рабочие письма", "type": "работа"},
    {"text": "Посмотреть лекцию по алгоритмам", "type": "учёба"},
    {"text": "Пробежка 3 км", "type": "спорт"},
    {"text": "Составить план на неделю", "type": "работа"},
    {"text": "Решить задачу на LeetCode", "type": "учёба"},
    {"text": "Отжимания 30 раз", "type": "спорт"},
    {"text": "Провести встречу с командой", "type": "работа"}
]

DATA_FILE = "tasks.json"

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.history = self.load_history()

        # Интерфейс
        self.create_widgets()
        self.update_task_list()

    def create_widgets(self):
        # Рамка генерации
        gen_frame = ttk.LabelFrame(self.root, text="Генератор задачи", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.generate_btn = ttk.Button(gen_frame, text="🎲 Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        self.current_task_label = ttk.Label(gen_frame, text="Нажмите кнопку", font=("Arial", 12, "bold"))
        self.current_task_label.pack(pady=5)

        # Рамка добавления новой задачи
        add_frame = ttk.LabelFrame(self.root, text="Добавить новую задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Описание:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_task_entry = ttk.Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Тип:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.type_var = tk.StringVar(value="учёба")
        type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, values=["учёба", "спорт", "работа"], state="readonly")
        type_combo.grid(row=1, column=1, padx=5, pady=5)

        add_btn = ttk.Button(add_frame, text="➕ Добавить", command=self.add_custom_task)
        add_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Рамка фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр по типу", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        self.filter_var = tk.StringVar(value="все")
        filter_all = ttk.Radiobutton(filter_frame, text="Все", variable=self.filter_var, value="все", command=self.update_task_list)
        filter_study = ttk.Radiobutton(filter_frame, text="Учёба", variable=self.filter_var, value="учёба", command=self.update_task_list)
        filter_sport = ttk.Radiobutton(filter_frame, text="Спорт", variable=self.filter_var, value="спорт", command=self.update_task_list)
        filter_work = ttk.Radiobutton(filter_frame, text="Работа", variable=self.filter_var, value="работа", command=self.update_task_list)

        filter_all.pack(side="left", padx=5)
        filter_study.pack(side="left", padx=5)
        filter_sport.pack(side="left", padx=5)
        filter_work.pack(side="left", padx=5)

        # История задач
        history_frame = ttk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side="right", fill="y")

        self.task_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=12)
        self.task_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Кнопка очистки истории
        clear_btn = ttk.Button(self.root, text="🗑 Очистить историю", command=self.clear_history)
        clear_btn.pack(pady=5)

    def load_history(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_history(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def generate_task(self):
        # Выбираем случайную задачу из предопределённых
        task = random.choice(PREDEFINED_TASKS)
        task_with_time = {
            "text": task["text"],
            "type": task["type"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(task_with_time)
        self.save_history()
        self.current_task_label.config(text=f"✅ {task['text']} ({task['type']})")
        self.update_task_list()

    def add_custom_task(self):
        new_text = self.new_task_entry.get().strip()
        if not new_text:
            messagebox.showwarning("Ошибка ввода", "Описание задачи не может быть пустым!")
            return

        task_type = self.type_var.get()
        new_task = {
            "text": new_text,
            "type": task_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(new_task)
        self.save_history()
        self.new_task_entry.delete(0, tk.END)
        self.update_task_list()
        messagebox.showinfo("Успех", "Задача добавлена!")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        filter_type = self.filter_var.get()
        for task in reversed(self.history):  # Показываем последние сверху
            if filter_type == "все" or task["type"] == filter_type:
                display_text = f"[{task['timestamp']}] {task['text']} ({task['type']})"
                self.task_listbox.insert(tk.END, display_text)

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю задач?"):
            self.history.clear()
            self.save_history()
            self.update_task_list()
            self.current_task_label.config(text="История очищена")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
