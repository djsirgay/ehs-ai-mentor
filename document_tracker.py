import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DocumentTracker:
    def __init__(self, data_file="tracker_data.json"):
        self.data_file = data_file
        self.processed_docs = {}  # hash -> document info
        self.assignment_history = {}  # user_id -> list of assignments
        self.load_data()
    
    def get_document_hash(self, text: str) -> str:
        """Creates document hash for duplicate detection"""
        # Take first 1000 characters for hashing
        content = text[:1000].strip().lower()
        return hashlib.md5(content.encode()).hexdigest()
    
    def is_duplicate(self, text: str) -> tuple[bool, Optional[Dict]]:
        """Checks if document was processed before"""
        doc_hash = self.get_document_hash(text)
        if doc_hash in self.processed_docs:
            return True, self.processed_docs[doc_hash]
        return False, None
    
    def save_document(self, text: str, assignments: List[Dict], skipped_duplicates: List[Dict] = None) -> str:
        """Saves information about processed document"""
        doc_hash = self.get_document_hash(text)
        
        self.processed_docs[doc_hash] = {
            "processed_at": datetime.now().isoformat(),
            "title": text[:100] + "..." if len(text) > 100 else text,
            "assignments_count": len(assignments),
            "assigned_users": [a["user_id"] for a in assignments],
            "skipped_duplicates": skipped_duplicates or []
        }
        
        # Save assignment history for each user
        for assignment in assignments:
            user_id = assignment["user_id"]
            if user_id not in self.assignment_history:
                self.assignment_history[user_id] = []
            
            self.assignment_history[user_id].append({
                "document_hash": doc_hash,
                "courses": assignment["courses_assigned"],
                "assigned_at": datetime.now().isoformat(),
                "reason": assignment.get("reason", "")
            })
        
        self.save_data()  # Сохраняем после обновления
        return doc_hash
    
    def get_user_history(self, user_id: str) -> List[Dict]:
        """Получает историю назначений для user"""
        return self.assignment_history.get(user_id, [])
    
    def has_recent_assignment(self, user_id: str, course_id: str, days: int = 30) -> bool:
        """Проверяет, назначался ли курс пользователю недавно"""
        history = self.get_user_history(user_id)
        
        for assignment in history:
            if course_id in assignment["courses"]:
                return True
        return False
    
    def get_all_user_courses(self, user_id: str) -> set:
        """Получает все когда-либо назначенные курсы"""
        all_courses = set()
        history = self.get_user_history(user_id)
        
        for assignment in history:
            all_courses.update(assignment["courses"])
        
        return all_courses
    
    def save_data(self):
        """Сохраняет данные в файл"""
        data = {
            "processed_docs": self.processed_docs,
            "assignment_history": self.assignment_history
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        """Загружает данные из file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.processed_docs = data.get("processed_docs", {})
                    self.assignment_history = data.get("assignment_history", {})
            except Exception as e:
                print(f"Error loading data: {e}")
                self.processed_docs = {}
                self.assignment_history = {}