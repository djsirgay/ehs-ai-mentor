import json
import os
from datetime import datetime
from typing import Dict, List

class AuditLogger:
    def __init__(self, log_file="audit_log.json"):
        self.log_file = log_file
        self.logs = []
        self.load_logs()
    
    def log_assignment(self, user_id: str, course_id: str, assigned_by: str = "AI", reason: str = "", priority: str = "normal"):
        """Logs course assignment"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "course_assigned",
            "user_id": user_id,
            "course_id": course_id,
            "assigned_by": assigned_by,
            "reason": reason,
            "priority": priority,
            "id": len(self.logs) + 1
        }
        
        self.logs.append(log_entry)
        self.save_logs()
    
    def log_document_processed(self, document_hash: str, assignments_count: int, protocol_title: str = ""):
        """Logs document processing"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "document_processed",
            "document_hash": document_hash,
            "protocol_title": protocol_title,
            "assignments_count": assignments_count,
            "processed_by": "AI",
            "id": len(self.logs) + 1
        }
        
        self.logs.append(log_entry)
        self.save_logs()
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Gets recent log entries"""
        return sorted(self.logs, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_user_history(self, user_id: str) -> List[Dict]:
        """Gets assignment history for user"""
        return [log for log in self.logs if log.get("user_id") == user_id and log["action"] == "course_assigned"]
    
    def save_logs(self):
        """Saves logs to file"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
    
    def load_logs(self):
        """Loads logs from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.logs = json.load(f)
            except Exception as e:
                print(f"Error loading logs: {e}")
                self.logs = []