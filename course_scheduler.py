from datetime import datetime, timedelta
from typing import Dict, List
import json

class CourseScheduler:
    def __init__(self):
        # Define course periodicity (in months)
        self.course_periods = {
            "HAZCOM-1910.1200": 12,  # Annually
            "Radiation Safety": 24,  # Every 2 years
            "X-Ray Safety Training": 24,  # Every 2 years
            "LAB-SAFETY-101": 12,  # Annually
            "RADIATION-ALARA-101": 24,  # Every 2 years
            "Radiation Safety Fundamentals": 24,  # Every 2 years
            "X-Ray Radiation Protection": 24,  # Every 2 years
        }
    
    def is_course_expired(self, course_id: str, assigned_date: str, buffer_days: int = 30) -> bool:
        """Checks if course has expired (with buffer for warning)"""
        if course_id not in self.course_periods:
            return False  # If period not defined, assume it doesn't expire
        
        try:
            assigned = datetime.fromisoformat(assigned_date.replace('Z', '+00:00'))
            period_months = self.course_periods[course_id]
            expiry_date = assigned + timedelta(days=period_months * 30)  # Approximately
            warning_date = expiry_date - timedelta(days=buffer_days)
            
            return datetime.now() >= warning_date
        except:
            return False
    
    def get_expired_courses(self, doc_tracker) -> List[Dict]:
        """Gets list of users with expiring courses"""
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
        """Determines if course needs to be reassigned due to expiration"""
        history = doc_tracker.get_user_history(user_id)
        
        for assignment in history:
            if course_id in assignment["courses"]:
                if self.is_course_expired(course_id, assignment["assigned_at"]):
                    return True
        
        return False