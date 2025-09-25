from bedrock_client import BedrockClient
from local_db import LocalDatabase

class AIMentor:
    def __init__(self):
        self.bedrock = BedrockClient()
        self.db = LocalDatabase()
    
    def analyze_and_assign(self, protocol_text: str, user_id: str):
        # Get user data
        user = self.db.get_user(user_id)
        if not user:
            return {"error": "User not found"}
        
        # Get completed courses
        completed_courses = self.db.get_user_courses(user_id)
        user_data = dict(user)
        user_data['completed_courses'] = completed_courses
        
        # Get all available courses
        courses = self.db.get_all_courses()
        
        # Analyze through AI
        decision = self.bedrock.analyze_protocol(protocol_text, user_data, courses)
        
        result = {
            "user_id": user_id,
            "analysis": decision,
            "assignments_made": []
        }
        
        # Assign courses if AI recommends
        if decision.get("should_assign") and decision.get("recommended_courses"):
            for course_id in decision["recommended_courses"]:
                # Check if course is already assigned
                existing = self.db.get_assignment_history(user_id, course_id)
                if not existing:
                    self.db.assign_course(user_id, course_id)
                    result["assignments_made"].append(course_id)
        
        return result
    
    def analyze_for_all_users(self, protocol_text: str, progress_callback=None):
        all_users = self.db.get_all_users()[:10]  # Only first 10 for demo
        courses = self.db.get_all_courses()
        
        results = {
            "protocol_summary": protocol_text[:200] + "...",
            "total_users": len(all_users),
            "assignments": []
        }
        
        for i, user in enumerate(all_users):
            if progress_callback:
                progress_callback(i + 1, len(all_users))
                
            user_id = user['user_id']
            completed_courses = self.db.get_user_courses(user_id)
            user_data = dict(user)
            user_data['completed_courses'] = completed_courses
            
            # AI analysis for each user
            decision = self.bedrock.analyze_protocol(protocol_text, user_data, courses)
            
            assignments_made = []
            if decision.get("should_assign") and decision.get("recommended_courses"):
                for course_id in decision["recommended_courses"]:
                    # Check local database
                    existing_db = self.db.get_assignment_history(user_id, course_id)
                    # Check document tracker history
                    existing_tracker = progress_callback and hasattr(progress_callback, '__self__') and hasattr(progress_callback.__self__, 'has_recent_assignment')
                    
                    if not existing_db:
                        self.db.assign_course(user_id, course_id)
                        assignments_made.append(course_id)
            
            if assignments_made:  # Only if there are assignments
                results["assignments"].append({
                    "user_id": user_id,
                    "name": user['name'],
                    "role": user['role'],
                    "department": user['department'],
                    "courses_assigned": assignments_made,
                    "reason": decision.get("reason", "")
                })
        
        return results
    
    def analyze_for_all_users_with_history(self, protocol_text: str, doc_tracker):
        all_users = self.db.get_all_users()[:10]  # Only first 10 for demo
        courses = self.db.get_all_courses()
        
        results = {
            "protocol_summary": protocol_text[:200] + "...",
            "total_users": len(all_users),
            "assignments": [],
            "skipped_duplicates": []
        }
        
        for i, user in enumerate(all_users):
            user_id = user['user_id']
            completed_courses = self.db.get_user_courses(user_id)
            user_data = dict(user)
            user_data['completed_courses'] = completed_courses
            
            # AI analysis for each user
            decision = self.bedrock.analyze_protocol(protocol_text, user_data, courses)
            
            assignments_made = []
            skipped_courses = []
            
            if decision.get("should_assign") and decision.get("recommended_courses"):
                for course_item in decision["recommended_courses"]:
                    # Support both formats
                    if isinstance(course_item, str):
                        course_id = course_item
                        priority = "normal"
                        renewal_months = 12
                        deadline_days = 30
                    else:
                        course_id = course_item.get("course_id", course_item)
                        priority = course_item.get("priority", "normal")
                        renewal_months = course_item.get("renewal_months", 12)
                        deadline_days = course_item.get("deadline_days", 30)
                    
                    existing_db = self.db.get_assignment_history(user_id, course_id)
                    existing_tracker = doc_tracker.has_recent_assignment(user_id, course_id)
                    all_user_courses = doc_tracker.get_all_user_courses(user_id)
                    course_expired = hasattr(self, '_scheduler') and self._scheduler.should_reassign_course(user_id, course_id, doc_tracker)
                    
                    if (existing_db or existing_tracker or course_id in all_user_courses) and not course_expired:
                        skipped_courses.append(course_id)
                    else:
                        self.db.assign_course(user_id, course_id)
                        assignments_made.append(course_id)
                        if course_expired:
                            assignments_made[-1] = f"{course_id} (update)"
                    
                    # Save AI-determined parameters
                    if hasattr(self, '_scheduler'):
                        self._scheduler.course_periods[course_id] = renewal_months
                        if not hasattr(self._scheduler, 'course_deadlines'):
                            self._scheduler.course_deadlines = {}
                        if not hasattr(self._scheduler, 'course_priorities'):
                            self._scheduler.course_priorities = {}
                        self._scheduler.course_deadlines[course_id] = deadline_days
                        self._scheduler.course_priorities[course_id] = priority
            
            if assignments_made:  # Only if there are new assignments
                # Collect period information
                course_periods = []
                if hasattr(self, '_scheduler'):
                    for course_id in assignments_made:
                        clean_course_id = course_id.replace(" (update)", "")
                        if clean_course_id in self._scheduler.course_periods:
                            course_periods.append({
                                "course_id": clean_course_id,
                                "priority": getattr(self._scheduler, 'course_priorities', {}).get(clean_course_id, "normal"),
                                "months": self._scheduler.course_periods[clean_course_id],
                                "deadline_days": getattr(self._scheduler, 'course_deadlines', {}).get(clean_course_id, 30)
                            })
                
                results["assignments"].append({
                    "user_id": user_id,
                    "name": user['name'],
                    "role": user['role'],
                    "department": user['department'],
                    "courses_assigned": assignments_made,
                    "reason": decision.get("reason", ""),
                    "course_periods": course_periods
                })
            
            if skipped_courses:  # If there are skipped courses
                results["skipped_duplicates"].append({
                    "user_id": user_id,
                    "name": user['name'],
                    "skipped_courses": skipped_courses,
                    "reason": "Courses were already assigned previously"
                })
        
        return results
    
    def chat(self, message: str, user_id: str = None) -> dict:
        """Smart chat with conversation memory"""
        try:
            # Get user context
            user_context = ""
            if user_id:
                user = self.db.get_user(user_id)
                if user:
                    user_context = f"User: {user['name']} ({user['role']}) from {user['department']}"
            
            # Get conversation history
            chat_history = self._get_chat_history(user_id) if user_id else []
            history_context = self._format_history(chat_history)
            
            # Create enhanced system prompt with memory
            system_prompt = f"""You are a helpful Random Coffee assistant for Cal Poly students.
You help with safety questions, workplace guidance, and campus information.
{user_context}

CONVERSATION HISTORY:
{history_context}

Be friendly, helpful, and remember the conversation context. If the user asks for elaboration or says "yes please", continue the previous topic."""
            
            response = self.bedrock.chat(message, system_prompt)
            
            # Save conversation to memory
            if user_id:
                self._save_to_history(user_id, message, response)
            
            return {"response": response}
            
        except Exception as e:
            return {"response": f"I'm here to help! Ask me about safety, workplace procedures, or campus life. (Error: {str(e)[:50]}...)"}
    
    def _get_chat_history(self, user_id: str) -> list:
        """Get recent chat history for user from persistent storage"""
        try:
            import json
            import os
            
            # Create chat history directory if it doesn't exist
            chat_dir = "data/chat_history"
            os.makedirs(chat_dir, exist_ok=True)
            
            # Load from file
            chat_file = f"{chat_dir}/{user_id}_chat.json"
            if os.path.exists(chat_file):
                with open(chat_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def _format_history(self, history: list) -> str:
        """Format chat history for AI context"""
        if not history:
            return "(No previous conversation)"
        
        # Show last 3 exchanges to keep context manageable
        recent = history[-6:] if len(history) > 6 else history
        formatted = []
        
        for i in range(0, len(recent), 2):
            if i + 1 < len(recent):
                user_msg = recent[i].split("] ", 1)[-1] if "] " in recent[i] else recent[i]
                ai_msg = recent[i + 1].split("] ", 1)[-1] if "] " in recent[i + 1] else recent[i + 1]
                formatted.append(f"User: {user_msg}\nAssistant: {ai_msg}")
        
        return "\n\n".join(formatted)
    
    def _save_to_history(self, user_id: str, user_message: str, ai_response: str):
        """Save conversation to persistent storage"""
        try:
            import json
            import os
            from datetime import datetime
            
            # Create chat history directory
            chat_dir = "data/chat_history"
            os.makedirs(chat_dir, exist_ok=True)
            
            # Load existing history
            chat_file = f"{chat_dir}/{user_id}_chat.json"
            history = []
            if os.path.exists(chat_file):
                with open(chat_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            # Add new messages with timestamp
            timestamp = datetime.now().isoformat()
            history.extend([
                f"[{timestamp}] {user_message}",
                f"[{timestamp}] {ai_response}"
            ])
            
            # Keep only last 20 messages (10 exchanges)
            if len(history) > 20:
                history = history[-20:]
            
            # Save to file
            with open(chat_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving chat history: {e}")
    
    def analyze_protocol(self, message: str) -> dict:
        """Alias for chat method to maintain compatibility"""
        return self.chat(message)