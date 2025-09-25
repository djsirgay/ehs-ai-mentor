import json
from datetime import datetime
from typing import Dict, List, Optional

class CoffeeMessenger:
    def __init__(self, data_file="coffee_messages.json"):
        self.data_file = data_file
        self.messages = self.load_messages()
    
    def load_messages(self) -> Dict:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_messages(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
    
    def send_message(self, match_id: str, sender_id: str, message: str, 
                    message_type: str = "text") -> Dict:
        if match_id not in self.messages:
            self.messages[match_id] = []
        
        message_obj = {
            "id": len(self.messages[match_id]) + 1,
            "sender_id": sender_id,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        self.messages[match_id].append(message_obj)
        self.save_messages()
        return message_obj
    
    def send_system_message(self, match_id: str, message: str) -> Dict:
        return self.send_message(match_id, "system", message, "system")
    
    def get_match_messages(self, match_id: str) -> List[Dict]:
        return self.messages.get(match_id, [])
    
    def mark_as_read(self, match_id: str, user_id: str):
        if match_id in self.messages:
            for message in self.messages[match_id]:
                if message["sender_id"] != user_id:
                    message["read"] = True
            self.save_messages()
    
    def confirm_meeting(self, match_id: str, time_slot: str):
        self.send_system_message(
            match_id, 
            f"✅ Meeting confirmed for {time_slot}! See you there!"
        )