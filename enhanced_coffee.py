import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

class EnhancedCoffeeManager:
    def __init__(self, data_file="enhanced_coffee_profiles.json", matches_file="enhanced_coffee_matches.json"):
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
    
    def create_enhanced_profile(self, user_id: str, name: str, role: str, department: str,
                               interests: List[str], availability: List[Dict], language: str = "en",
                               personality_traits: List[str] = None, meeting_preferences: Dict = None) -> Dict:
        profile = {
            "user_id": user_id,
            "name": name,
            "role": role,
            "department": department,
            "interests": interests,
            "availability": availability,
            "language": language,
            "personality_traits": personality_traits or [],
            "meeting_preferences": meeting_preferences or {},
            "active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "match_history": [],
            "compatibility_scores": {}
        }
        
        self.profiles[user_id] = profile
        self.save_profiles()
        return profile
    
    def calculate_compatibility_score(self, user1_id: str, user2_id: str) -> Tuple[float, Dict]:
        profile1 = self.profiles.get(user1_id)
        profile2 = self.profiles.get(user2_id)
        
        if not profile1 or not profile2:
            return 0.0, {}
        
        # Интересы (40%)
        interests1 = set(profile1.get("interests", []))
        interests2 = set(profile2.get("interests", []))
        common_interests = interests1 & interests2
        interest_score = len(common_interests) / max(len(interests1 | interests2), 1) * 0.4
        
        # Департамент (20%)
        dept_score = 0.2 if profile1.get("department") == profile2.get("department") else 0.1
        
        # Роль (15%)
        role_score = 0.15 if profile1.get("role") != profile2.get("role") else 0.05  # Разные роли лучше
        
        # Личностные черты (15%)
        traits1 = set(profile1.get("personality_traits", []))
        traits2 = set(profile2.get("personality_traits", []))
        trait_score = len(traits1 & traits2) / max(len(traits1 | traits2), 1) * 0.15
        
        # Доступность (10%)
        avail_score = 0.1  # Упрощенно
        
        total_score = interest_score + dept_score + role_score + trait_score + avail_score
        
        breakdown = {
            "interests": interest_score,
            "department": dept_score,
            "role": role_score,
            "personality": trait_score,
            "availability": avail_score,
            "common_interests": list(common_interests)
        }
        
        return min(total_score, 1.0), breakdown
    
    def create_ai_matches(self, max_matches: int = 20) -> List[Dict]:
        active_profiles = [p for p in self.profiles.values() if p.get("active", False)]
        
        if len(active_profiles) < 2:
            return []
        
        # Вычисляем совместимость для всех пар
        compatibility_pairs = []
        for i, profile1 in enumerate(active_profiles):
            for profile2 in active_profiles[i+1:]:
                score, breakdown = self.calculate_compatibility_score(
                    profile1["user_id"], profile2["user_id"]
                )
                compatibility_pairs.append({
                    "users": [profile1["user_id"], profile2["user_id"]],
                    "score": score,
                    "breakdown": breakdown
                })
        
        # Сортируем по совместимости
        compatibility_pairs.sort(key=lambda x: x["score"], reverse=True)
        
        # Создаем матчи
        matches = []
        used_users = set()
        
        for pair in compatibility_pairs[:max_matches]:
            user1, user2 = pair["users"]
            if user1 not in used_users and user2 not in used_users:
                match_id = str(uuid.uuid4())
                match = {
                    "id": match_id,
                    "users": [user1, user2],
                    "compatibility_score": pair["score"],
                    "compatibility_breakdown": pair["breakdown"],
                    "status": "active",
                    "created_at": datetime.now().isoformat(),
                    "confirmed_time": None,
                    "feedback": []
                }
                
                self.matches[match_id] = match
                matches.append(match)
                used_users.add(user1)
                used_users.add(user2)
        
        self.save_matches()
        return matches
    
    def get_user_insights(self, user_id: str) -> Dict:
        profile = self.profiles.get(user_id)
        if not profile:
            return {}
        
        user_matches = [m for m in self.matches.values() if user_id in m["users"]]
        
        # Статистика
        total_matches = len(user_matches)
        avg_compatibility = sum(m.get("compatibility_score", 0) for m in user_matches) / max(total_matches, 1)
        
        # Популярные интересы среди партнеров
        partner_interests = []
        for match in user_matches:
            partner_id = next((uid for uid in match["users"] if uid != user_id), None)
            if partner_id and partner_id in self.profiles:
                partner_interests.extend(self.profiles[partner_id].get("interests", []))
        
        interest_counts = {}
        for interest in partner_interests:
            interest_counts[interest] = interest_counts.get(interest, 0) + 1
        
        return {
            "total_matches": total_matches,
            "average_compatibility": round(avg_compatibility, 2),
            "popular_partner_interests": sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "match_success_rate": len([m for m in user_matches if m["status"] == "confirmed"]) / max(total_matches, 1)
        }