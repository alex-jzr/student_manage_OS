import os
import json

class Students:
    # 使用类变量定义文件路径
    JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students_info.json')
    
    def __init__(self, sid, name, age):
        self.sid = str(sid)
        self.name = name
        self.age = age

    def ToList(self):
        return [self.sid, self.name, self.age]
    
    @classmethod
    def _ensure_file_exists(cls):
        """确保JSON文件存在且有效"""
        if not os.path.exists(cls.JSON_FILE):
            with open(cls.JSON_FILE, 'w') as f:
                json.dump([], f)
        else:
            # 验证文件内容是否有效
            try:
                with open(cls.JSON_FILE, 'r') as f:
                    json.load(f)
            except json.JSONDecodeError:
                with open(cls.JSON_FILE, 'w') as f:
                    json.dump([], f)

    @classmethod
    def search_student(cls, sid, return_stile=True):
        cls._ensure_file_exists()
        try:
            with open(cls.JSON_FILE, 'r') as f:
                students = json.load(f)
                found = next((s for s in students if str(sid) == str(s['sid'])), None)
                
                if return_stile:
                    return found is not None
                return f"学号：{found['sid']} 姓名：{found['name']} 年龄：{found['age']}" if found else '该学生不存在'
                
        except Exception as e:
            return f'查询出错: {str(e)}'

    @classmethod
    def to_json(cls, info_list):
        cls._ensure_file_exists()
        try:
            sid = str(info_list[0])
            
            # 读取现有数据
            with open(cls.JSON_FILE, 'r+') as f:
                students = json.load(f)
                
                if any(str(s['sid']) == sid for s in students):
                    return '该学生已存在'
                    
                students.append({
                    'sid': sid,
                    'name': info_list[1],
                    'age': info_list[2]
                })
                
                f.seek(0)
                json.dump(students, f, indent=4)
                f.truncate()
                
            return '学生信息已添加'
            
        except Exception as e:
            return f'操作失败: {str(e)}'
        
#    student1 = Students('000002', 'Alice', 18)
#    Students.ToJson(Students.ToList(student1))
