from datetime import datetime, timedelta

def generate_user_dashboard_html(user_data, assignments, scheduler, course_completion=None):


    """Генерирует HTML страницу пользователя"""
    
    user = user_data["user"]
    
    # Группируем курсы по статусам
    active_courses = []
    expired_courses = []
    upcoming_deadlines = []
    
    for assignment in assignments:
        course_id = assignment.get("course_id")
        if course_id:
            is_expired = assignment.get("is_expired", False)
            assigned_date = datetime.fromisoformat(assignment["timestamp"].replace('Z', '+00:00'))
            
            # Вычисляем дедлайн
            deadline_days = assignment.get("deadline_days", 30)
            deadline_date = assigned_date + timedelta(days=deadline_days)
            days_left = (deadline_date - datetime.now()).days
            
            is_completed = assignment.get("is_completed", False)
            
            course_info = {
                "course_id": course_id,
                "assigned_date": assigned_date.strftime("%d.%m.%Y"),
                "deadline_date": deadline_date.strftime("%d.%m.%Y"),
                "days_left": days_left,
                "priority": assignment.get("priority", "normal"),
                "reason": assignment.get("reason", ""),
                "renewal_months": assignment.get("renewal_months", "N/A"),
                "is_completed": is_completed
            }
            
            if is_completed:
                # Пройденные курсы не показываем в активных
                pass
            elif is_expired:
                expired_courses.append(course_info)
            elif days_left <= 7:
                upcoming_deadlines.append(course_info)
            else:
                active_courses.append(course_info)
    
    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Личный кабинет - {user["name"]}</title>
    <style>
        body {{ font-family: Arial; max-width: 900px; margin: 20px auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: #007bff; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .stats {{ display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; flex: 1; min-width: 150px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .course-section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .course-item {{ background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .priority-critical {{ border-left-color: #dc3545; }}
        .priority-high {{ border-left-color: #fd7e14; }}
        .priority-normal {{ border-left-color: #28a745; }}
        .priority-low {{ border-left-color: #6c757d; }}
        .deadline-urgent {{ background: #f8d7da; border-left-color: #dc3545; }}
        .deadline-soon {{ background: #fff3cd; border-left-color: #ffc107; }}
        .status-badge {{ padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .status-active {{ background: #d4edda; color: #155724; }}
        .status-urgent {{ background: #f8d7da; color: #721c24; }}
        .status-expired {{ background: #f5c6cb; color: #721c24; }}
        h1, h2, h3 {{ color: #333; }}
        .back-btn {{ background: #6c757d; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <button class="back-btn" onclick="window.history.back()">← Назад к системе</button>
    
    <div class="header">
        <h1>👤 Личный кабинет</h1>
        <h2>{user["name"]} ({user["user_id"]})</h2>
        <p><strong>Должность:</strong> {user["role"]} | <strong>Отдел:</strong> {user["department"]}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #28a745;">{len(active_courses)}</div>
            <div style="font-size: 12px; color: #666;">✅ Активных</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #007bff;">{sum(1 for a in assignments if a.get('is_completed', False))}</div>
            <div style="font-size: 12px; color: #666;">✅ Завершено</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #ffc107;">{len(upcoming_deadlines)}</div>
            <div style="font-size: 12px; color: #666;">⚠️ Скоро дедлайн</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #dc3545;">{len(expired_courses)}</div>
            <div style="font-size: 12px; color: #666;">❌ Просрочено</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #6f42c1;">{len(assignments)}</div>
            <div style="font-size: 12px; color: #666;">📚 Всего</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 24px; font-weight: bold; color: #fd7e14;">{len([c for c in active_courses + upcoming_deadlines if c.get('priority') == 'critical'])}</div>
            <div style="font-size: 12px; color: #666;">🔴 Критичных</div>
        </div>
    </div>
    '''
    
    # Срочные дедлайны
    if upcoming_deadlines:
        html += '''
    <div class="course-section">
        <h3>⚠️ Срочные дедлайны (менее 7 дней)</h3>
        '''
        for course in upcoming_deadlines:
            priority_class = f"priority-{course['priority']}"
            if course['days_left'] <= 3:
                deadline_class = "deadline-urgent"
                status_badge = '<span class="status-badge status-urgent">🚨 СРОЧНО</span>'
            else:
                deadline_class = "deadline-soon"
                status_badge = '<span class="status-badge status-urgent">⚠️ СКОРО</span>'
            
            html += f'''
        <div class="course-item {priority_class} {deadline_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>📚 {course["course_id"]}</strong>
                {status_badge}
            </div>
            <div style="font-size: 14px;">
                <strong>⏰ Дедлайн:</strong> {course["deadline_date"]} ({course["days_left"]} дн.)<br>
                <strong>🎯 Приоритет:</strong> {course["priority"]}<br>
                <strong>📅 Назначен:</strong> {course["assigned_date"]}
            </div>
            {f'<div style="margin-top: 8px; font-style: italic; color: #666;">💡 {course["reason"]}</div>' if course["reason"] else ''}
            <div style="margin-top: 10px;">
                <button onclick="completeCourse('{course["course_id"]}')" style="background: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">✅ Отметить как пройденный</button>
            </div>
        </div>
            '''
        html += '</div>'
    
    # Активные курсы
    if active_courses:
        html += '''
    <div class="course-section">
        <h3>✅ Активные курсы</h3>
        '''
        for course in active_courses:
            priority_class = f"priority-{course['priority']}"
            status_badge = '<span class="status-badge status-active">✅ АКТИВЕН</span>'
            
            html += f'''
        <div class="course-item {priority_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>📚 {course["course_id"]}</strong>
                {status_badge}
            </div>
            <div style="font-size: 14px;">
                <strong>⏰ Дедлайн:</strong> {course["deadline_date"]} ({course["days_left"]} дн.)<br>
                <strong>🎯 Приоритет:</strong> {course["priority"]}<br>
                <strong>🔄 Обновление:</strong> каждые {course["renewal_months"]} мес.<br>
                <strong>📅 Назначен:</strong> {course["assigned_date"]}
            </div>
            {f'<div style="margin-top: 8px; font-style: italic; color: #666;">💡 {course["reason"]}</div>' if course["reason"] else ''}
            <div style="margin-top: 10px;">
                <button onclick="completeCourse('{course["course_id"]}')" style="background: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer;">✅ Отметить как пройденный</button>
            </div>
        </div>
            '''
        html += '</div>'
    
    # Просроченные курсы
    if expired_courses:
        html += '''
    <div class="course-section">
        <h3>❌ Просроченные курсы</h3>
        '''
        for course in expired_courses:
            priority_class = f"priority-{course['priority']}"
            status_badge = '<span class="status-badge status-expired">❌ ПРОСРОЧЕН</span>'
            
            html += f'''
        <div class="course-item {priority_class}" style="background: #f8d7da;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>📚 {course["course_id"]}</strong>
                {status_badge}
            </div>
            <div style="font-size: 14px;">
                <strong>⏰ Просрочен на:</strong> {abs(course["days_left"])} дн.<br>
                <strong>🎯 Приоритет:</strong> {course["priority"]}<br>
                <strong>📅 Назначен:</strong> {course["assigned_date"]}
            </div>
            {f'<div style="margin-top: 8px; font-style: italic; color: #666;">💡 {course["reason"]}</div>' if course["reason"] else ''}
        </div>
            '''
        html += '</div>'
    
    # Завершенные курсы
    completed_courses = [a for a in assignments if a.get('is_completed', False)]
    if completed_courses:
        html += '''
    <div class="course-section">
        <h3>✅ Завершенные курсы</h3>
        '''
        for assignment in completed_courses:
            course_id = assignment.get("course_id")
            assigned_date = datetime.fromisoformat(assignment["timestamp"].replace('Z', '+00:00')).strftime("%d.%m.%Y")
            priority = assignment.get("priority", "normal")
            priority_class = f"priority-{priority}"
            
            # Находим дату завершения
            completion_info = None
            if course_completion:
                completion_info = next((c for c in course_completion.completions if c["user_id"] == user["user_id"] and c["course_id"] == course_id), None)
            completed_date = "N/A"
            if completion_info:
                completed_date = datetime.fromisoformat(completion_info["completed_at"]).strftime("%d.%m.%Y")
            
            html += f'''
        <div class="course-item {priority_class}" style="background: #d4edda; border-left-color: #28a745;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong>📚 {course_id}</strong>
                <span class="status-badge" style="background: #d4edda; color: #155724;">✅ ЗАВЕРШЕН</span>
            </div>
            <div style="font-size: 14px;">
                <strong>📅 Назначен:</strong> {assigned_date}<br>
                <strong>✅ Завершен:</strong> {completed_date}<br>
                <strong>🎯 Приоритет:</strong> {priority}
            </div>
            {f'<div style="margin-top: 8px; font-style: italic; color: #666;">💡 {assignment.get("reason", "")}</div>' if assignment.get("reason") else ''}
        </div>
            '''
        html += '</div>'
    
    if not assignments:
        html += '''
    <div class="course-section">
        <p style="text-align: center; color: #666; font-style: italic;">
            📚 У вас пока нет назначенных курсов
        </p>
    </div>
        '''
    
    html += '''
    <div style="text-align: center; margin-top: 30px; padding: 20px; background: white; border-radius: 10px;">
        <p style="color: #666; font-size: 14px;">
            🤖 Курсы назначаются автоматически на основе анализа протоколов безопасности<br>
            📧 При новых назначениях вы получите уведомление
        </p>
    </div>
    
    <script>
        async function completeCourse(courseId) {
            const userId = window.location.pathname.split('/')[2]; // Извлекаем user_id из URL
            
            try {
                const response = await fetch('/complete-course', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `user_id=${userId}&course_id=${courseId}`
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    location.reload(); // Перезагружаем страницу
                } else {
                    alert('⚠️ ' + data.message);
                }
                
            } catch (error) {
                console.error('Error:', error);
                alert('❌ Ошибка при отметке курса');
            }
        }
    </script>
</body>
</html>
    '''
    
    return html