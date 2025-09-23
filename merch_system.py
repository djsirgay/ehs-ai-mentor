import json
from datetime import datetime
from typing import List, Dict, Optional
import random

class MerchSystem:
    def __init__(self):
        self.merch_file = "merch_catalog.json"
        self.events_file = "merch_events.json"
        self.catalog = self.load_catalog()
        self.events = self.load_events()
    
    def load_catalog(self) -> List[Dict]:
        """Загружает каталог мерча"""
        try:
            with open(self.merch_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Создаем базовый каталог Cal Poly мерча
            default_catalog = [
                # Cal Poly Mustang Shop (Follett) - deeplinks
                {
                    "id": "calpoly-hoodie-001",
                    "name": "Cal Poly Mustangs Hoodie",
                    "description": "Official Cal Poly Mustangs pullover hoodie with embroidered logo",
                    "price": 54.99,
                    "image": "🏫",
                    "source": "mustang_shop",
                    "category": "apparel",
                    "tags": ["official", "hoodie", "mustangs", "campus"],
                    "course_tags": ["general", "campus-wide"],
                    "dept_tags": ["all"],
                    "url": "https://calpoly.bkstr.com/product/cal-poly-mustangs-hoodie",
                    "utm_params": "utm_source=ehs_mentor&utm_medium=merch&utm_campaign=post_course",
                    "external": True
                },
                {
                    "id": "calpoly-tshirt-001", 
                    "name": "Cal Poly Engineering T-Shirt",
                    "description": "College of Engineering pride tee with department logo",
                    "price": 24.99,
                    "image": "👕",
                    "source": "mustang_shop",
                    "category": "apparel",
                    "tags": ["engineering", "tshirt", "department"],
                    "course_tags": ["engineering", "lab-safety", "hazwoper"],
                    "dept_tags": ["engineering", "environmental"],
                    "url": "https://calpoly.bkstr.com/product/engineering-tshirt",
                    "utm_params": "utm_source=ehs_mentor&utm_medium=merch&utm_campaign=post_course",
                    "external": True
                },
                {
                    "id": "safety-mug-001",
                    "name": "Safety First Coffee Mug",
                    "description": "Custom EHS-themed mug with safety slogans",
                    "price": 16.99,
                    "image": "☕",
                    "source": "custom_pod",
                    "category": "accessories",
                    "tags": ["safety", "coffee", "custom", "ehs"],
                    "course_tags": ["osha", "lab-safety", "fire-safety"],
                    "dept_tags": ["all"],
                    "customizable": True,
                    "external": False
                },
                {
                    "id": "lab-notebook-001",
                    "name": "Cal Poly Lab Safety Notebook",
                    "description": "Professional lab notebook with safety guidelines",
                    "price": 12.99,
                    "image": "📓",
                    "source": "mustang_shop",
                    "category": "supplies",
                    "tags": ["lab", "notebook", "safety", "professional"],
                    "course_tags": ["lab-safety", "biosafety", "chem-safety"],
                    "dept_tags": ["chemistry", "biology", "engineering"],
                    "url": "https://calpoly.bkstr.com/product/lab-notebook",
                    "utm_params": "utm_source=ehs_mentor&utm_medium=merch&utm_campaign=course_completion",
                    "external": True
                },
                # Fanatics items
                {
                    "id": "fanatics-cap-001",
                    "name": "Cal Poly Mustangs Adjustable Cap",
                    "description": "Official NCAA licensed cap with Cal Poly Mustangs logo",
                    "price": 29.99,
                    "image": "🧢",
                    "source": "fanatics",
                    "category": "accessories",
                    "tags": ["cap", "hat", "mustangs", "ncaa"],
                    "course_tags": ["outdoor", "field-work"],
                    "dept_tags": ["agriculture", "engineering"],
                    "url": "https://www.fanatics.com/college/cal-poly-mustangs/cal-poly-mustangs-cap",
                    "utm_params": "utm_source=ehs_mentor&utm_medium=merch&utm_campaign=celebration",
                    "external": True
                },
                {
                    "id": "custom-badge-001",
                    "name": "Course Completion Badge",
                    "description": "Custom enamel pin celebrating your safety training achievement",
                    "price": 8.99,
                    "image": "🏅",
                    "source": "custom_pod",
                    "category": "collectibles",
                    "tags": ["badge", "pin", "achievement", "custom"],
                    "course_tags": ["all"],
                    "dept_tags": ["all"],
                    "customizable": True,
                    "badge_gate": True,
                    "external": False
                }
            ]
            self.save_catalog(default_catalog)
            return default_catalog
    
    def save_catalog(self, catalog: List[Dict]):
        """Сохраняет каталог в файл"""
        with open(self.merch_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        self.catalog = catalog
    
    def load_events(self) -> List[Dict]:
        """Загружает события мерча"""
        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_events(self):
        """Сохраняет события в файл"""
        with open(self.events_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
    
    def get_post_course_recommendations(self, user_id: str, course_id: str, user_data: Dict) -> List[Dict]:
        """Получает рекомендации мерча после завершения course"""
        
        # Логируем событие завершения course
        self.log_event("course_completed", user_id, {"course_id": course_id})
        
        # Получаем теги course для матчинга
        course_tags = self._get_course_tags(course_id)
        dept = user_data.get("department", "").lower()
        role = user_data.get("role", "").lower()
        
        # Скоринг товаров
        scored_items = []
        for item in self.catalog:
            score = self._calculate_item_score(item, course_tags, dept, role, "post_course")
            if score > 0:
                item_copy = item.copy()
                item_copy["score"] = score
                item_copy["context"] = "post_course_celebration"
                scored_items.append(item_copy)
        
        # Сортируем по скору и берем топ-6
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        recommendations = scored_items[:6]
        
        # Добавляем UTM параметры для внешних ссылок
        for item in recommendations:
            if item.get("external") and item.get("url"):
                utm = item.get("utm_params", "")
                separator = "&" if "?" in item["url"] else "?"
                item["tracking_url"] = f"{item['url']}{separator}{utm}"
        
        return recommendations
    
    def get_course_merch_tab(self, course_id: str, user_data: Dict) -> List[Dict]:
        """Получает мерч для вкладки в карточке course"""
        course_tags = self._get_course_tags(course_id)
        dept = user_data.get("department", "").lower()
        role = user_data.get("role", "").lower()
        
        scored_items = []
        for item in self.catalog:
            score = self._calculate_item_score(item, course_tags, dept, role, "course_tab")
            if score > 0:
                item_copy = item.copy()
                item_copy["score"] = score
                item_copy["context"] = "course_merch_tab"
                scored_items.append(item_copy)
        
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        return scored_items[:4]  # Топ-4 для вкладки
    
    def get_personalized_feed(self, user_data: Dict, completed_courses: List[str]) -> List[Dict]:
        """Получает персонализированную ленту мерча"""
        dept = user_data.get("department", "").lower()
        role = user_data.get("role", "").lower()
        
        # Собираем теги из всех пройденных курсов
        all_course_tags = set()
        for course_id in completed_courses:
            all_course_tags.update(self._get_course_tags(course_id))
        
        scored_items = []
        for item in self.catalog:
            score = self._calculate_item_score(item, list(all_course_tags), dept, role, "profile_feed")
            if score > 0:
                item_copy = item.copy()
                item_copy["score"] = score
                item_copy["context"] = "personalized_feed"
                scored_items.append(item_copy)
        
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        return scored_items[:12]  # Топ-12 для ленты
    
    def _get_course_tags(self, course_id: str) -> List[str]:
        """Получает теги course для матчинга с мерчем"""
        course_lower = course_id.lower()
        tags = []
        
        # Маппинг курсов на теги
        if "osha" in course_lower:
            tags.extend(["osha", "safety", "general"])
        if "lab-safety" in course_lower or "biosafety" in course_lower:
            tags.extend(["lab-safety", "laboratory", "science"])
        if "fire" in course_lower:
            tags.extend(["fire-safety", "emergency"])
        if "hazwoper" in course_lower or "hazmat" in course_lower:
            tags.extend(["hazwoper", "hazmat", "environmental"])
        if "ppe" in course_lower:
            tags.extend(["ppe", "protective", "safety"])
        if "ergonomic" in course_lower:
            tags.extend(["ergonomics", "workplace"])
        if "radiation" in course_lower or "laser" in course_lower:
            tags.extend(["radiation", "laser", "physics"])
        
        # Общие теги для всех курсов
        tags.extend(["safety", "training", "professional"])
        
        return list(set(tags))  # Убираем дубликаты
    
    def _calculate_item_score(self, item: Dict, course_tags: List[str], dept: str, role: str, context: str) -> int:
        """Вычисляет скор товара для рекомендации"""
        score = 0
        
        # Базовый скор
        score += 10
        
        # Совпадение тегов course (+30 за каждое совпадение)
        item_course_tags = item.get("course_tags", [])
        for tag in course_tags:
            if tag in item_course_tags:
                score += 30
        
        # Совпадение департамента (+20)
        item_dept_tags = item.get("dept_tags", [])
        if dept in item_dept_tags or "all" in item_dept_tags:
            score += 20
        
        # Контекстные бонусы
        if context == "post_course":
            # После course приоритет кастомным и памятным вещам
            if item.get("customizable"):
                score += 25
            if "achievement" in item.get("tags", []):
                score += 20
        
        elif context == "course_tab":
            # В курсе приоритет практичным вещам
            if item.get("category") in ["supplies", "accessories"]:
                score += 15
        
        # Свежесть (новые товары получают бонус)
        if item.get("new", False):
            score += 10
        
        # Популярность (можно добавить позже на основе статистики)
        popularity = item.get("popularity", 0)
        score += popularity * 2
        
        return score
    
    def log_event(self, event_type: str, user_id: str, data: Dict = None):
        """Логирует событие мерча"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "data": data or {}
        }
        self.events.append(event)
        self.save_events()
    
    def track_merch_interaction(self, user_id: str, item_id: str, action: str, context: str = None):
        """Трекает взаимодействие с мерчем"""
        self.log_event(f"merch_{action}", user_id, {
            "item_id": item_id,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_analytics(self) -> Dict:
        """Получает аналитику по мерчу"""
        total_events = len(self.events)
        
        # Группируем по типам событий
        event_counts = {}
        for event in self.events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Топ товаров по взаимодействиям
        item_interactions = {}
        for event in self.events:
            if event["event_type"].startswith("merch_"):
                item_id = event.get("data", {}).get("item_id")
                if item_id:
                    item_interactions[item_id] = item_interactions.get(item_id, 0) + 1
        
        return {
            "total_events": total_events,
            "event_counts": event_counts,
            "top_items": sorted(item_interactions.items(), key=lambda x: x[1], reverse=True)[:10]
        }