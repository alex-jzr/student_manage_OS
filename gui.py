import tkinter as tk
from tkinter import ttk, messagebox
from class_students import Students
import os
import json

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("学生信息管理系统")
        self.root.geometry("800x600")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 设置字体
        self.font_title = ('Microsoft YaHei', 14, 'bold')
        self.font_normal = ('Microsoft YaHei', 10)
        
        # 确保数据文件存在
        self.ensure_data_file()
        
        self.create_widgets()
        self.load_students()
        
    def create_widgets(self):
        """创建所有GUI组件"""
        # 顶部标题
        self.header = ttk.Label(
            self.root, 
            text="学生信息管理系统", 
            font=self.font_title,
            foreground="#2c3e50"
        )
        self.header.pack(pady=20)
        
        # 操作面板框架
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 输入字段
        ttk.Label(self.control_frame, text="学号:", font=self.font_normal).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.sid_entry = ttk.Entry(self.control_frame, font=self.font_normal)
        self.sid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="姓名:", font=self.font_normal).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(self.control_frame, font=self.font_normal)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="年龄:", font=self.font_normal).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.age_entry = ttk.Entry(self.control_frame, font=self.font_normal)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 按钮
        self.add_btn = ttk.Button(
            self.control_frame, 
            text="添加学生", 
            command=self.add_student,
            style='Accent.TButton'
        )
        self.add_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.search_btn = ttk.Button(
            self.control_frame, 
            text="查询学生", 
            command=self.search_student
        )
        self.search_btn.grid(row=1, column=2, padx=5, pady=5)
        
        self.delete_btn = ttk.Button(
            self.control_frame, 
            text="删除学生", 
            command=self.delete_student,
            style='Danger.TButton'
        )
        self.delete_btn.grid(row=2, column=2, padx=5, pady=5)
        
        self.clear_btn = ttk.Button(
            self.control_frame, 
            text="清空输入", 
            command=self.clear_entries
        )
        self.clear_btn.grid(row=0, column=3, padx=5, pady=5)
        
        self.refresh_btn = ttk.Button(
            self.control_frame, 
            text="刷新列表", 
            command=self.load_students
        )
        self.refresh_btn.grid(row=1, column=3, padx=5, pady=5)
        
        # 学生列表
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('sid', 'name', 'age'),
            show='headings',
            selectmode='browse'
        )
        
        # 设置列
        self.tree.heading('sid', text='学号', anchor=tk.CENTER)
        self.tree.heading('name', text='姓名', anchor=tk.CENTER)
        self.tree.heading('age', text='年龄', anchor=tk.CENTER)
        
        self.tree.column('sid', width=150, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('age', width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 自定义样式
        self.style.configure('Accent.TButton', foreground='white', background='#3498db')
        self.style.configure('Danger.TButton', foreground='white', background='#e74c3c')
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_tree_double_click)

    def ensure_data_file(self):
        """确保数据文件存在且有效"""
        if not os.path.exists(Students.JSON_FILE):
            with open(Students.JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)    
    
    def load_students(self):
        """加载所有学生到树形视图"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # 从JSON文件加载数据
            with open(Students.JSON_FILE, 'r', encoding='utf-8') as f:
                students = json.load(f)
            
            if not isinstance(students, list):
                messagebox.showerror("错误", "数据格式不正确，应该是一个列表！")
                return
            
            for student in students:
                # 确保每个学生都有所有必要字段
                if all(key in student for key in ['sid', 'name', 'age']):
                    self.tree.insert('', tk.END, values=(
                        student['sid'], 
                        student['name'], 
                        student['age']
                    ))
                else:
                    print(f"跳过无效的学生记录: {student}")
                    
            if not students:
                self.tree.insert('', tk.END, values=(
                    "暂无数据", "", ""
                ))
                
        except Exception as e:
            messagebox.showerror("错误", f"加载学生数据失败: {str(e)}")

    def add_student(self):
        """添加新学生"""
        sid = self.sid_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        
        if not all([sid, name, age]):
            messagebox.showwarning("警告", "请填写所有字段！")
            return
        
        try:
            # 尝试转换为整数，验证年龄有效性
            age_int = int(age)
            if age_int <= 0:
                raise ValueError("年龄必须大于0")
        except ValueError:
            messagebox.showwarning("警告", "年龄必须是有效的正整数！")
            return
        
        result = Students.to_json([sid, name, age_int])  # 直接传递整数
        messagebox.showinfo("结果", result)
        self.clear_entries()
        self.load_students()
    
    def search_student(self):
        """查询学生"""
        sid = self.sid_entry.get()
        if not sid:
            messagebox.showwarning("警告", "请输入学号！")
            return
        
        students = Students.search_student(sid, return_stile=False)
        if isinstance(students, str):  # 如果返回的是错误信息
            messagebox.showerror("错误", students)
            return
        
        if not students:
            messagebox.showinfo("结果", f"未找到学号为 {sid} 的学生")
        else:
            student = students[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, student['name'])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, student['age'])
    
    def delete_student(self):
        """删除学生"""
        sid = self.sid_entry.get()
        if not sid:
            messagebox.showwarning("警告", "请输入学号！")
            return
        
        confirm = messagebox.askyesno("确认", f"确定要删除学号为 {sid} 的学生吗？")
        if not confirm:
            return
        
        success = Students.delete_student(sid)
        if success:
            messagebox.showinfo("结果", "学生删除成功！")
            self.clear_entries()
            self.load_students()
        else:
            messagebox.showinfo("结果", f"未找到学号为 {sid} 的学生")
    
    def clear_entries(self):
        """清空输入框"""
        self.sid_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
    
    def on_tree_double_click(self, event):
        """树形视图双击事件"""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.sid_entry.delete(0, tk.END)
            self.sid_entry.insert(0, values[0])
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, values[2])

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()