import csv
import json
from typing import List, Dict, Optional

class LocalDatabase:
    def __init__(self):
        self.users = []
        self.courses = []
        self.user_courses = []
        self.load_data()
    
    def load_data(self):
        # Загружаем пользователей
        with open('data/users.csv', 'r') as f:
            reader = csv.DictReader(f)
            self.users = list(reader)
        
        # Загружаем курсы
        with open('data/courses.csv', 'r') as f:
            reader = csv.DictReader(f)
            self.courses = list(reader)
        
        # Загружаем назначения курсов
        with open('data/user_courses.csv', 'r') as f:
            reader = csv.DictReader(f)
            self.user_courses = list(reader)
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        for user in self.users:
            if user['user_id'] == user_id:
                return user
        return None
    
    def get_user_courses(self, user_id: str) -> List[str]:
        return [uc['course_id'] for uc in self.user_courses if uc['user_id'] == user_id]
    
    def get_all_courses(self) -> List[Dict]:
        return self.courses
    
    def assign_course(self, user_id: str, course_id: str):
        # Проверяем, не назначен ли уже курс
        for uc in self.user_courses:
            if uc['user_id'] == user_id and uc['course_id'] == course_id:
                return  # Уже назначен
        
        # Добавляем новое назначение
        self.user_courses.append({
            'user_id': user_id,
            'course_id': course_id,
            'completed_on': ''
        })
    
    def get_assignment_history(self, user_id: str, course_id: str) -> Optional[Dict]:
        for uc in self.user_courses:
            if uc['user_id'] == user_id and uc['course_id'] == course_id:
                return uc
        return None
    
    def get_all_users(self) -> List[Dict]:
        return self.users