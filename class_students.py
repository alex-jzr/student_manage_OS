import os
import json
from typing import Union, List, Dict

class Students:
    # 使用类变量定义文件路径
    JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students_info.json')
    
    # 定义统一的编码常量
    ENCODING = 'utf-8'
    
    def __init__(self, sid: Union[str, int], name: str, age: Union[int, str]):
        self.sid = str(sid)
        self.name = name
        # 确保年龄为整数
        self.age = int(age) if isinstance(age, str) and age.isdigit() else int(age)
    
    def to_list(self) -> List[Union[str, int]]:
        return [self.sid, self.name, self.age]
    
    @classmethod
    def _ensure_file_exists(cls):
        """确保JSON文件存在且有效，完全支持中文"""
        if not os.path.exists(cls.JSON_FILE):
            with open(cls.JSON_FILE, 'w', encoding=cls.ENCODING) as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        else:
            try:
                with open(cls.JSON_FILE, 'r', encoding=cls.ENCODING) as f:
                    data = json.load(f)
                    # 修复现有数据中的年龄类型问题
                    if isinstance(data, list):
                        modified = False
                        for student in data:
                            if isinstance(student.get('age'), str) and student['age'].isdigit():
                                student['age'] = int(student['age'])
                                modified = True
                        if modified:
                            with open(cls.JSON_FILE, 'w', encoding=cls.ENCODING) as f_write:
                                json.dump(data, f_write, ensure_ascii=False, indent=4)
            except (json.JSONDecodeError, UnicodeDecodeError):
                with open(cls.JSON_FILE, 'w', encoding=cls.ENCODING) as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
                    
    @classmethod
    def search_student(cls, sid: Union[str, int], return_style: bool = True) -> Union[bool, List[Dict], str]:
        """查询学生信息，完全支持中文"""
        cls._ensure_file_exists()
        try:
            with open(cls.JSON_FILE, 'r', encoding=cls.ENCODING) as f:
                students = json.load(f)
                found_students = [s for s in students if str(sid) == str(s['sid'])]
                
                if return_style:
                    return len(found_students) > 0
                return found_students
                
        except Exception as e:
            return f'查询出错: {str(e)}'
        
    @classmethod
    def to_json(cls, info_list: List[Union[str, int]]) -> str:
        """添加学生信息到JSON文件，支持中文"""
        cls._ensure_file_exists()
        try:
            sid = str(info_list[0])
            name = str(info_list[1])
            # 确保年龄为整数
            age = int(info_list[2]) if isinstance(info_list[2], str) and info_list[2].isdigit() else int(info_list[2])
            
            with open(cls.JSON_FILE, 'r+', encoding=cls.ENCODING) as f:
                students = json.load(f)
                
                if any(str(s['sid']) == sid for s in students):
                    return '该学生已存在'
                    
                students.append({
                    'sid': sid,
                    'name': name,
                    'age': age  # 确保存储为整数
                })
                
                f.seek(0)
                json.dump(students, f, ensure_ascii=False, indent=4)
                f.truncate()
                
            return '学生信息已添加'
            
        except ValueError:
            return '年龄必须是有效数字'
        except Exception as e:
            return f'操作失败: {str(e)}'
        
    @staticmethod
    def delete_student(sid: Union[str, int]) -> bool:
        """删除指定学号的学生，支持中文"""
        try:
            with open(Students.JSON_FILE, 'r', encoding=Students.ENCODING) as f:
                students = json.load(f)
            
            original_count = len(students)
            students = [student for student in students if student['sid'] != str(sid)]
            
            if len(students) == original_count:
                return False
            
            with open(Students.JSON_FILE, 'w', encoding=Students.ENCODING) as f:
                json.dump(students, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            print(f"删除学生失败: {e}")
            return False

# 测试部分
if __name__ == "__main__":
    # 创建一个学生实例
    student1 = Students('000002', 'Alex', 16)


