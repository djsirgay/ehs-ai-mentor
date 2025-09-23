import json
from datetime import datetime
from typing import List, Dict, Optional

class BadgeSystem:
    def __init__(self):
        self.badges_file = "user_badges.json"
        self.badge_rules_file = "badge_rules.json"
        self.user_badges = self.load_user_badges()
        self.badge_rules = self.load_badge_rules()
    
    def load_user_badges(self) -> Dict:
        try:
            with open(self.badges_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def load_badge_rules(self) -> List[Dict]:
        try:
            with open(self.badge_rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Создаем базовые правила для бейджей
            default_rules = [
                {
                    "badge_id": "safety_champion",
                    "name": "Safety Champion",
                    "description": "Complete 5 safety courses",
                    "emoji": "🏆",
                    "type": "course_completion",
                    "requirements": {
                        "course_count": 5,
                        "course_tags": ["safety"]
                    },
                    "unlocks_merch": ["custom-badge-001", "champion-hoodie-001"]
                },
                {
                    "badge_id": "lab_expert",
                    "name": "Lab Safety Expert", 
                    "description": "Master all lab safety courses",
                    "emoji": "🧪",
                    "type": "course_completion",
                    "requirements": {
                        "specific_courses": ["LAB-SAFETY-101", "BIOSAFETY-201", "CHEM-SPILL-101"]
                    },
                    "unlocks_merch": ["lab-coat-custom-001", "expert-badge-001"]
                },
                {
                    "badge_id": "fire_marshal",
                    "name": "Fire Safety Marshal",
                    "description": "Complete fire safety training with excellence",
                    "emoji": "🔥",
                    "type": "course_completion",
                    "requirements": {
                        "course_tags": ["fire-safety"],
                        "min_score": 95
                    },
                    "unlocks_merch": ["fire-marshal-badge-001", "emergency-kit-001"]
                },
                {
                    "badge_id": "early_adopter",
                    "name": "Early Adopter",
                    "description": "One of the first 100 users of EHS AI Mentor",
                    "emoji": "🚀",
                    "type": "milestone",
                    "requirements": {
                        "user_rank": 100
                    },
                    "unlocks_merch": ["early-adopter-tshirt-001", "founder-badge-001"]
                },
                {
                    "badge_id": "streak_master",
                    "name": "Streak Master",
                    "description": "Complete courses 7 days in a row",
                    "emoji": "⚡",
                    "type": "streak",
                    "requirements": {
                        "consecutive_days": 7
                    },
                    "unlocks_merch": ["streak-hoodie-001", "lightning-badge-001"]
                },
                {
                    "badge_id": "mentor",
                    "name": "Safety Mentor",
                    "description": "Help 10 colleagues through Random Coffee",
                    "emoji": "🎓",
                    "type": "social",
                    "requirements": {
                        "coffee_meetings": 10,
                        "avg_rating": 4.5
                    },
                    "unlocks_merch": ["mentor-badge-001", "leadership-book-001"]
                }
            ]
            self.save_badge_rules(default_rules)
            return default_rules
    
    def save_user_badges(self):
        with open(self.badges_file, 'w', encoding='utf-8') as f:
            json.dump(self.user_badges, f, ensure_ascii=False, indent=2)
    
    def save_badge_rules(self, rules: List[Dict]):
        with open(self.badge_rules_file, 'w', encoding='utf-8') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
        self.badge_rules = rules
    
    def check_and_award_badges(self, user_id: str, user_data: Dict, completed_courses: List[str], 
                              coffee_stats: Dict = None) -> List[Dict]:
        """Проверяет и присваивает новые бейджи пользователю"""
        
        if user_id not in self.user_badges:
            self.user_badges[user_id] = []
        
        current_badges = [b["badge_id"] for b in self.user_badges[user_id]]
        new_badges = []
        
        for rule in self.badge_rules:
            badge_id = rule["badge_id"]
            
            # Пропускаем уже полученные бейджи
            if badge_id in current_badges:
                continue
            
            # Проверяем условия получения бейджа
            if self._check_badge_requirements(rule, user_data, completed_courses, coffee_stats):
                badge = {
                    "badge_id": badge_id,
                    "name": rule["name"],
                    "description": rule["description"],
                    "emoji": rule["emoji"],
                    "earned_at": datetime.now().isoformat(),
                    "unlocks_merch": rule.get("unlocks_merch", [])
                }
                
                self.user_badges[user_id].append(badge)
                new_badges.append(badge)
        
        if new_badges:
            self.save_user_badges()
        
        return new_badges
    
    def _check_badge_requirements(self, rule: Dict, user_data: Dict, completed_courses: List[str], 
                                 coffee_stats: Dict = None) -> bool:
        """Проверяет выполнение требований для получения бейджа"""
        
        requirements = rule.get("requirements", {})
        badge_type = rule.get("type")
        
        if badge_type == "course_completion":
            # Проверка по количеству курсов
            if "course_count" in requirements:
                required_count = requirements["course_count"]
                course_tags = requirements.get("course_tags", [])
                
                if course_tags:
                    # Подсчитываем курсы с определенными тегами
                    matching_courses = 0
                    for course_id in completed_courses:
                        if any(tag in course_id.lower() for tag in course_tags):
                            matching_courses += 1
                    return matching_courses >= required_count
                else:
                    return len(completed_courses) >= required_count
            
            # Проверка конкретных курсов
            if "specific_courses" in requirements:
                required_courses = requirements["specific_courses"]
                return all(course in completed_courses for course in required_courses)
        
        elif badge_type == "milestone":
            # Проверка ранга user (для Early Adopter)
            if "user_rank" in requirements:
                # Здесь можно добавить логику определения ранга user
                return True  # Упрощенная логика
        
        elif badge_type == "social":
            # Проверка социальных достижений
            if coffee_stats and "coffee_meetings" in requirements:
                meetings = coffee_stats.get("total_meetings", 0)
                avg_rating = coffee_stats.get("average_rating", 0)
                
                return (meetings >= requirements["coffee_meetings"] and 
                       avg_rating >= requirements.get("avg_rating", 0))
        
        elif badge_type == "streak":
            # Проверка серий (упрощенная логика)
            if "consecutive_days" in requirements:
                # Здесь можно добавить логику проверки серий
                return len(completed_courses) >= requirements["consecutive_days"]
        
        return False
    
    def get_user_badges(self, user_id: str) -> List[Dict]:
        """Получает все бейджи user"""
        return self.user_badges.get(user_id, [])
    
    def get_unlocked_merch(self, user_id: str) -> List[str]:
        """Получает список разблокированного мерча для user"""
        user_badges = self.get_user_badges(user_id)
        unlocked_merch = []
        
        for badge in user_badges:
            unlocked_merch.extend(badge.get("unlocks_merch", []))
        
        return list(set(unlocked_merch))  # Убираем дубликаты
    
    def can_access_merch(self, user_id: str, merch_id: str) -> bool:
        """Проверяет, может ли пользователь получить доступ к товару"""
        unlocked_merch = self.get_unlocked_merch(user_id)
        return merch_id in unlocked_merch
    
    def get_badge_progress(self, user_id: str, user_data: Dict, completed_courses: List[str], 
                          coffee_stats: Dict = None) -> List[Dict]:
        """Получает прогресс по всем бейджам"""
        
        current_badges = [b["badge_id"] for b in self.get_user_badges(user_id)]
        progress = []
        
        for rule in self.badge_rules:
            badge_id = rule["badge_id"]
            
            if badge_id in current_badges:
                progress.append({
                    "badge_id": badge_id,
                    "name": rule["name"],
                    "emoji": rule["emoji"],
                    "status": "earned",
                    "progress": 100
                })
            else:
                # Вычисляем прогресс
                progress_percent = self._calculate_badge_progress(rule, user_data, completed_courses, coffee_stats)
                progress.append({
                    "badge_id": badge_id,
                    "name": rule["name"],
                    "emoji": rule["emoji"],
                    "description": rule["description"],
                    "status": "in_progress",
                    "progress": progress_percent,
                    "unlocks_merch": rule.get("unlocks_merch", [])
                })
        
        return progress
    
    def _calculate_badge_progress(self, rule: Dict, user_data: Dict, completed_courses: List[str], 
                                 coffee_stats: Dict = None) -> int:
        """Вычисляет прогресс получения бейджа в процентах"""
        
        requirements = rule.get("requirements", {})
        badge_type = rule.get("type")
        
        if badge_type == "course_completion":
            if "course_count" in requirements:
                required_count = requirements["course_count"]
                course_tags = requirements.get("course_tags", [])
                
                if course_tags:
                    matching_courses = sum(1 for course_id in completed_courses 
                                         if any(tag in course_id.lower() for tag in course_tags))
                    return min(int((matching_courses / required_count) * 100), 100)
                else:
                    return min(int((len(completed_courses) / required_count) * 100), 100)
            
            if "specific_courses" in requirements:
                required_courses = requirements["specific_courses"]
                completed_required = sum(1 for course in required_courses if course in completed_courses)
                return int((completed_required / len(required_courses)) * 100)
        
        elif badge_type == "social" and coffee_stats:
            if "coffee_meetings" in requirements:
                meetings = coffee_stats.get("total_meetings", 0)
                required_meetings = requirements["coffee_meetings"]
                return min(int((meetings / required_meetings) * 100), 100)
        
        return 0