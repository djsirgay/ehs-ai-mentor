import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class RandomCoffeeManager:
    def __init__(self, data_file="coffee_profiles.json", matches_file="coffee_matches.json"):
        self.data_file = data_file
        self.matches_file = matches_file
        self.profiles = self.load_profiles()
        self.matches = self.load_matches()
    
    def load_profiles(self) -> Dict:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_profiles(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)
    
    def load_matches(self) -> Dict:
        try:
            with open(self.matches_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_matches(self):
        with open(self.matches_file, 'w', encoding='utf-8') as f:
            json.dump(self.matches, f, ensure_ascii=False, indent=2)
    
    def create_profile(self, user_id: str, name: str, role: str, department: str, 
                      interests: List[str], availability: List[Dict], language: str = "en") -> Dict:
        profile = {
            "user_id": user_id,
            "name": name,
            "role": role,
            "department": department,
            "interests": interests,
            "availability": availability,
            "language": language,
            "active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.profiles[user_id] = profile
        self.save_profiles()
        return profile
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        return self.profiles.get(user_id)
    
    def update_profile(self, user_id: str, updates: Dict) -> bool:
        if user_id in self.profiles:
            self.profiles[user_id].update(updates)
            self.profiles[user_id]["updated_at"] = datetime.now().isoformat()
            self.save_profiles()
            return True
        return False
    
    def create_weekly_matches(self) -> List[Dict]:
        active_profiles = [p for p in self.profiles.values() if p.get("active", False)]
        
        if len(active_profiles) < 2:
            return []
        
        matches = []
        used_users = set()
        
        for i, profile1 in enumerate(active_profiles):
            if profile1["user_id"] in used_users:
                continue
                
            for profile2 in active_profiles[i+1:]:
                if profile2["user_id"] in used_users:
                    continue
                
                # Простой алгоритм матчинга
                if self._can_match(profile1, profile2):
                    match_id = str(uuid.uuid4())
                    match = {
                        "id": match_id,
                        "users": [profile1["user_id"], profile2["user_id"]],
                        "status": "active",
                        "created_at": datetime.now().isoformat(),
                        "confirmed_time": None,
                        "feedback": []
                    }
                    
                    self.matches[match_id] = match
                    matches.append(match)
                    used_users.add(profile1["user_id"])
                    used_users.add(profile2["user_id"])
                    break
        
        self.save_matches()
        return matches
    
    def _can_match(self, profile1: Dict, profile2: Dict) -> bool:
        # Простая логика матчинга
        common_interests = set(profile1.get("interests", [])) & set(profile2.get("interests", []))
        return len(common_interests) > 0 or profile1.get("department") == profile2.get("department")
    
    def get_user_matches(self, user_id: str) -> List[Dict]:
        return [match for match in self.matches.values() if user_id in match["users"]]
    
    def confirm_match(self, match_id: str, timeslot: str) -> bool:
        if match_id in self.matches:
            self.matches[match_id]["status"] = "confirmed"
            self.matches[match_id]["confirmed_time"] = timeslot
            self.save_matches()
            return True
        return False
    
    def add_feedback(self, match_id: str, user_id: str, rating: int, 
                    safety_discussed: bool = False, tags: List[str] = None):
        if match_id in self.matches:
            feedback = {
                "user_id": user_id,
                "rating": rating,
                "safety_discussed": safety_discussed,
                "tags": tags or [],
                "timestamp": datetime.now().isoformat()
            }
            self.matches[match_id]["feedback"].append(feedback)
            self.save_matches()
    
    def get_stats(self) -> Dict:
        total_profiles = len(self.profiles)
        active_profiles = len([p for p in self.profiles.values() if p.get("active", False)])
        total_matches = len(self.matches)
        confirmed_matches = len([m for m in self.matches.values() if m["status"] == "confirmed"])
        
        return {
            "total_profiles": total_profiles,
            "active_profiles": active_profiles,
            "total_matches": total_matches,
            "confirmed_matches": confirmed_matches
        }