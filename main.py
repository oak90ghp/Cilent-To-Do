import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cilent To-Do")
        self.root.geometry("1000x600")  
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("TLabel", font=("Segoe UI", 12))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))
        
        # Task storage
        self.tasks = []
        self.data_file = "tasks.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10, fill=tk.X, padx=20)
        
        header_label = ttk.Label(header_frame, text="Cilent To-Do", style="Header.TLabel")
        header_label.pack(anchor=tk.W)
        
        # Task input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.task_entry = ttk.Entry(input_frame, font=("Segoe UI", 12))
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.focus()
        
        add_button = ttk.Button(input_frame, text="添加任务", command=self.add_task)
        add_button.pack(side=tk.RIGHT)
        
        # Task list frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task list
        self.task_listbox = tk.Listbox(list_frame, font=("Segoe UI", 12), selectbackground="#a6a6a6",
                                      yscrollcommand=scrollbar.set, selectmode=tk.SINGLE,
                                      bg="#f0f0f0", bd=0, highlightthickness=0)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Bind double click to toggle completion
        self.task_listbox.bind("<Double-1>", self.toggle_task_complete)
        
        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, fill=tk.X, padx=20)

        # 添加底部文字
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, pady=5)
        footer_label = ttk.Label(footer_frame, text="Cilent To-Do是一个开源的App，您可以在Github上找到该项目，部分内容使用了Trae AI编写(Github仓库：https://github.com/oak90ghp/Cilent-To-Do)", font=("Segoe UI", 8), foreground="#888888")
        footer_label.pack()
        
        complete_button = ttk.Button(button_frame, text="标记为完成", command=self.mark_complete)
        complete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_button = ttk.Button(button_frame, text="删除此任务", command=self.delete_task)
        delete_button.pack(side=tk.LEFT)

        save_as_button = ttk.Button(button_frame, text="另存为", command=self.save_as_task)
        save_as_button.pack(side=tk.LEFT, padx=(10, 0))

        open_button = ttk.Button(button_frame, text="打开", command=self.open_task)
        open_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Update the task list display
        self.update_task_list()
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                "id": len(self.tasks) + 1,
                "text": task_text,
                "complete": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(task)
            self.save_tasks()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cilent To-Do", "请输入任务内容")
    
    def mark_complete(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]["complete"] = not self.tasks[index]["complete"]
            self.save_tasks()
            self.update_task_list()
    
    def toggle_task_complete(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]["complete"] = not self.tasks[index]["complete"]
            self.save_tasks()
            self.update_task_list()
    
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            # Reassign IDs to maintain consistency
            for i, task in enumerate(self.tasks):
                task["id"] = i + 1
            self.save_tasks()
            self.update_task_list()
        else:
            messagebox.showwarning("Cilent To-Do", "请选择一项要删除的任务")
    
    def save_as_task(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON格式的任务清单", "*.json"), ("任意格式", "*")]
        )
        if file_path:
            self.save_tasks(file_path)
            messagebox.showinfo("Cilent To-Do", f"任务已保存至: {file_path}")

    def open_task(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON格式的任务清单", "*.json"), ("任意格式", "*")]
        )
        if file_path:
            self.load_tasks(file_path)
            self.update_task_list()
            messagebox.showinfo("Cilent To-Do", f"已打开任务文件: {file_path}")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = task["text"]
            if task["complete"]:
                display_text = f"✓ {display_text}"
                self.task_listbox.insert(tk.END, display_text)
                self.task_listbox.itemconfig(tk.END, fg="#888888", strike=1)
            else:
                self.task_listbox.insert(tk.END, display_text)
    
    def save_tasks(self, file_path=None):
        if file_path is None:
            file_path = self.data_file
        try:
            with open(file_path, "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            messagebox.showerror("Cilent To-Do", f"无法保存该任务: {str(e)}")
    
    def load_tasks(self, file_path=None):
        if file_path is None:
            file_path = self.data_file
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    self.tasks = json.load(f)
        except Exception as e:
            messagebox.showerror("Cilent To-Do", f"无法加载任务清单: {str(e)}")
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()