from datetime import datetime, timedelta
from typing import Dict, List
import json

class CourseScheduler:
    def __init__(self):
        # Определяем периодичность курсов (в месяцах)
        self.course_periods = {
            "HAZCOM-1910.1200": 12,  # Ежегодно
            "Radiation Safety": 24,  # Раз в 2 года
            "X-Ray Safety Training": 24,  # Раз в 2 года
            "LAB-SAFETY-101": 12,  # Ежегодно
            "RADIATION-ALARA-101": 24,  # Раз в 2 года
            "Radiation Safety Fundamentals": 24,  # Раз в 2 года
            "X-Ray Radiation Protection": 24,  # Раз в 2 года
        }
    
    def is_course_expired(self, course_id: str, assigned_date: str, buffer_days: int = 30) -> bool:
        """Проверяет, истек ли срок курса (с буфером для предупреждения)"""
        if course_id not in self.course_periods:
            return False  # Если период не определен, считаем что не истекает
        
        try:
            assigned = datetime.fromisoformat(assigned_date.replace('Z', '+00:00'))
            period_months = self.course_periods[course_id]
            expiry_date = assigned + timedelta(days=period_months * 30)  # Приблизительно
            warning_date = expiry_date - timedelta(days=buffer_days)
            
            return datetime.now() >= warning_date
        except:
            return False
    
    def get_expired_courses(self, doc_tracker) -> List[Dict]:
        """Получает список пользователей с истекающими курсами"""
        expired_list = []
        
        for user_id, history in doc_tracker.assignment_history.items():
            user_expired = []
            
            for assignment in history:
                for course_id in assignment["courses"]:
                    if self.is_course_expired(course_id, assignment["assigned_at"]):
                        user_expired.append({
                            "course_id": course_id,
                            "assigned_at": assignment["assigned_at"],
                            "period_months": self.course_periods.get(course_id, 0)
                        })
            
            if user_expired:
                expired_list.append({
                    "user_id": user_id,
                    "expired_courses": user_expired
                })
        
        return expired_list
    
    def should_reassign_course(self, user_id: str, course_id: str, doc_tracker) -> bool:
        """Определяет, нужно ли переназначить курс из-за истечения срока"""
        history = doc_tracker.get_user_history(user_id)
        
        for assignment in history:
            if course_id in assignment["courses"]:
                if self.is_course_expired(course_id, assignment["assigned_at"]):
                    return True
        
        return False