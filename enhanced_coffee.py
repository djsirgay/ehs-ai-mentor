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
    
    def can_create_matches(self, user_id: str = None) -> Tuple[bool, str, str]:
        """Проверяет, можно ли создавать новые матчи. Возвращает (can_create, message, next_date)"""
        from datetime import datetime, timedelta
        
        # Если пользователь не указан или у него нет профиля, разрешаем создание матчей
        if not user_id or user_id not in self.profiles:
            return True, "", ""
        
        now = datetime.now()
        
        # Получаем последний матч любого пользователя
        latest_match = None
        for match in self.matches.values():
            match_date = datetime.fromisoformat(match["created_at"].replace('Z', ''))
            if not latest_match or match_date > latest_match:
                latest_match = match_date
        
        if latest_match:
            # Проверяем, прошла ли неделя с последнего матча
            days_since = (now - latest_match).days
            if days_since < 7:
                next_match_date = latest_match + timedelta(days=7)
                next_date_str = next_match_date.strftime("%B %d, %Y")
                days_left = 7 - days_since
                
                return False, f"🌟 Hey there! I love your enthusiasm for meeting new people! ☕\n\n📅 **Here's how Random Coffee works:** We create thoughtful matches once a week to give you time to really connect with each person. Your next matching opportunity is on {next_date_str} ({days_left} days left).\n\n🤝 **Why weekly?** This gives you time to have meaningful conversations, maybe grab that coffee, and build genuine friendships!\n\n🚀 **In the meantime, I'd love to be your friend and safety assistant!** I can help with:\n• Workplace safety questions\n• Course recommendations\n• Cal Poly campus tips\n• Just friendly conversation!\n\nWhat would you like to chat about? ✨", next_date_str
        
        return True, "", ""
    
    def create_ai_matches(self, max_matches: int = 20, user_id: str = None) -> List[Dict]:
        # Проверяем еженедельное ограничение
        can_create, message, _ = self.can_create_matches(user_id)
        if not can_create:
            return []
        
        active_profiles = [p for p in self.profiles.values() if p.get("active", False)]
        
        if len(active_profiles) < 2:
            return []
        
        # Получаем существующие пары пользователей
        existing_pairs = set()
        for match in self.matches.values():
            users = sorted(match["users"])
            existing_pairs.add((users[0], users[1]))
        
        # Вычисляем совместимость для всех пар (исключая существующие)
        compatibility_pairs = []
        for i, profile1 in enumerate(active_profiles):
            for profile2 in active_profiles[i+1:]:
                user1_id = profile1["user_id"]
                user2_id = profile2["user_id"]
                
                # Проверяем, что эта пара еще не существует
                pair_key = tuple(sorted([user1_id, user2_id]))
                if pair_key not in existing_pairs:
                    score, breakdown = self.calculate_compatibility_score(user1_id, user2_id)
                    compatibility_pairs.append({
                        "users": [user1_id, user2_id],
                        "score": score,
                        "breakdown": breakdown
                    })
        
        # Сортируем по совместимости
        compatibility_pairs.sort(key=lambda x: x["score"], reverse=True)
        
        # Создаем матчи (только новые пары)
        matches = []
        created_count = 0
        
        for pair in compatibility_pairs:
            if created_count >= max_matches:
                break
                
            user1, user2 = pair["users"]
            match_id = str(uuid.uuid4())
            match = {
                "id": match_id,
                "users": [user1, user2],
                "compatibility_score": pair["score"],
                "compatibility_breakdown": pair["breakdown"],
                "status": "confirmed",  # Автоматически подтверждаем
                "created_at": datetime.now().isoformat(),
                "confirmed_time": datetime.now().isoformat(),
                "feedback": []
            }
            
            self.matches[match_id] = match
            matches.append(match)
            created_count += 1
        
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