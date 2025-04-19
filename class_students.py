import os
import json

class Students:
    # 使用类变量定义文件路径
    JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students_info.json')
    
    def __init__(self, sid, name, age):
        self.sid = str(sid)
        self.name = name
        self.age = age

    def to_list(self):
        return [self.sid, self.name, self.age]
    
    # 在 class_students.py 中修改 _ensure_file_exists 方法
    @classmethod
    def _ensure_file_exists(cls):
        """确保JSON文件存在且有效"""
        if not os.path.exists(cls.JSON_FILE):
            with open(cls.JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
        else:
            try:
                with open(cls.JSON_FILE, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError:
                with open(cls.JSON_FILE, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False)
                    
    @classmethod
    def search_student(cls, sid, return_stile=True):
        cls._ensure_file_exists()
        try:
            with open(cls.JSON_FILE, 'r', encoding='utf-8') as f:  # 添加编码参数
                students = json.load(f)
                found_students = [s for s in students if str(sid) == str(s['sid'])]
                
                if return_stile:
                    return len(found_students) > 0  # 返回布尔值表示是否找到
                return found_students  # 返回学生字典的列表
                
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
        
    @staticmethod
    def delete_student(sid):
        """删除指定学号的学生"""
        try:
            # 读取现有的学生数据
            with open(Students.JSON_FILE, 'r', encoding='utf-8') as f:  # 添加编码参数
                students = json.load(f)
            
            # 如果没有找到要删除的学生，返回 False
            original_count = len(students)
            students = [student for student in students if student['sid'] != sid]
            
            if len(students) == original_count:
                return False
            
            # 更新 JSON 文件，保存新的学生数据
            with open(Students.JSON_FILE, 'w', encoding='utf-8') as f:  # 添加编码参数
                json.dump(students, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            print(f"删除学生失败: {e}")
            return False

# 测试部分
if __name__ == "__main__":
    # 创建一个学生实例
    student1 = Students('000002', 'Alex', 16)


