import json
import os
from datetime import datetime
from typing import Dict, List

class CourseCompletion:
    def __init__(self, completion_file="course_completions.json"):
        self.completion_file = completion_file
        self.completions = []
        self.load_completions()
    
    def complete_course(self, user_id: str, course_id: str, completion_method: str = "manual"):
        """Отмечает курс как пройденный"""
        completion_entry = {
            "user_id": user_id,
            "course_id": course_id,
            "completed_at": datetime.now().isoformat(),
            "completion_method": completion_method,  # manual, automatic, etc.
            "id": len(self.completions) + 1
        }
        
        self.completions.append(completion_entry)
        self.save_completions()
        return completion_entry
    
    def is_course_completed(self, user_id: str, course_id: str) -> bool:
        """Проверяет, пройден ли курс пользователем"""
        return any(
            c["user_id"] == user_id and c["course_id"] == course_id 
            for c in self.completions
        )
    
    def get_user_completions(self, user_id: str) -> List[Dict]:
        """Получает все завершенные курсы пользователя"""
        return [c for c in self.completions if c["user_id"] == user_id]
    
    def get_completion_stats(self) -> Dict:
        """Получает статистику завершений"""
        total_completions = len(self.completions)
        unique_users = len(set(c["user_id"] for c in self.completions))
        unique_courses = len(set(c["course_id"] for c in self.completions))
        
        return {
            "total_completions": total_completions,
            "unique_users": unique_users,
            "unique_courses": unique_courses
        }
    
    def save_completions(self):
        """Сохраняет завершения в файл"""
        with open(self.completion_file, 'w', encoding='utf-8') as f:
            json.dump(self.completions, f, ensure_ascii=False, indent=2)
    
    def load_completions(self):
        """Загружает завершения из файла"""
        if os.path.exists(self.completion_file):
            try:
                with open(self.completion_file, 'r', encoding='utf-8') as f:
                    self.completions = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки завершений: {e}")
                self.completions = []