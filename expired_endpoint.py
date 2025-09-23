@app.get("/expired-courses")
async def get_expired_courses():
    """Получить список пользователей с истекающими courseми"""
    expired_list = scheduler.get_expired_courses(doc_tracker)
    
    # Получаем информацию о userх
    for item in expired_list:
        user = mentor.db.get_user(item["user_id"])
        if user:
            item["user_name"] = user["name"]
            item["role"] = user["role"]
            item["department"] = user["department"]
    
    return {
        "expired_count": len(expired_list),
        "expired_users": expired_list
    }