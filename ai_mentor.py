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