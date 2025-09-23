from datetime import datetime, timedelta

def generate_user_dashboard_html(user_data, assignments, scheduler, course_completion=None):


    """Генерирует HTML страницу user"""
    
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
                "assigned_date": assigned_date.strftime("%m/%d/%Y"),
                "deadline_date": deadline_date.strftime("%m/%d/%Y"),
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
    <link rel="stylesheet" href="/tahoe.css">
    <style>
    :root {{
      --space-xs: clamp(0.5rem, 1vw, 0.75rem);
      --space-s: clamp(0.75rem, 2vw, 1rem);
      --space-m: clamp(1rem, 3vw, 1.5rem);
      --space-l: clamp(1.5rem, 4vw, 2rem);
      --space-xl: clamp(2rem, 6vw, 3rem);
      --space-xxl: clamp(3rem, 8vw, 4rem);
      
      --text-xs: clamp(0.875rem, 2vw, 1rem);
      --text-s: clamp(1rem, 2.5vw, 1.125rem);
      --text-m: clamp(1.125rem, 3vw, 1.25rem);
      --text-l: clamp(1.5rem, 4vw, 2rem);
      --text-xl: clamp(2rem, 6vw, 3rem);
      --text-xxl: clamp(3rem, 8vw, 4rem);
      
      --gray-50: #fafafa;
      --gray-100: #f5f5f5;
      --gray-200: #e5e5e5;
      --gray-300: #d4d4d4;
      --gray-400: #a3a3a3;
      --gray-500: #737373;
      --gray-600: #525252;
      --gray-700: #404040;
      --gray-800: #262626;
      --gray-900: #171717;
      
      --container-max: 1200px;
      --container-pad: 20px;
      
      --bg: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ecfdf5 100%);
      --panel: #ffffff;
      --ink: var(--gray-800);
      --muted: var(--gray-600);
      --brand: #0e7a4e;
      --brand-light: #16a34a;
      --brand-dark: #0d5f3c;
      --accent: #3b82f6;
      --success: #10b981;
      --warning: #f59e0b;
      --error: #ef4444;
      --blue: #3b82f6;
      --purple: #8b5cf6;
      --orange: #f97316;
      --red: #ef4444;
      --shadow-1: 0 3px 10px rgba(0,0,0,.08);
      --shadow-2: 0 8px 24px rgba(0,0,0,.12);
      --speed: .2s;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: var(--text-s);
      line-height: 1.6;
      color: var(--gray-800);
      background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 50%, #86efac 100%);
      min-height: 100vh;
      padding: 0;
    }}

    .container {{
      max-width: var(--container-max);
      margin: 0 auto;
      padding: 0 var(--container-pad);
    }}
    
    .hero{{
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin: var(--space-l) 0;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    .hero h1{{
      font-size: var(--text-xl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }}
    
    h1 {{
      font-size: var(--text-xxl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }}

    h2 {{
      font-size: var(--text-xl);
      font-weight: 600;
      line-height: 1.2;
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-900);
    }}

    h3 {{
      font-size: var(--text-l);
      font-weight: 600;
      line-height: 1.3;
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-800);
    }}

    p {{
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-600);
    }}
    
    button {{
      border: none;
      border-radius: 10px;
      padding: var(--space-s) var(--space-m);
      font-weight: 600;
      font-size: var(--text-xs);
      cursor: pointer;
      transition: all var(--speed);
      background: linear-gradient(135deg, var(--brand) 0%, #16a34a 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(14, 122, 78, 0.3);
    }}
    
    button:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(14, 122, 78, 0.4);
    }}
    
    button:active {{
      transform: translateY(0) scale(0.98);
    }}
    
    .tahoe-stat-card {{
      background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
      padding: var(--space-s);
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.8);
    }}
    
    .tahoe-stat-card:hover {{
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .training-card {{
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin-bottom: var(--space-m);
      display: flex;
      align-items: center;
      gap: var(--space-m);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.3);
      position: relative;
      overflow: hidden;
    }}
    
    .training-card::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--brand);
      border-radius: 4px 0 0 4px;
    }}
    
    .training-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }}
    
    .course-item {{
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin-bottom: var(--space-m);
      display: flex;
      align-items: center;
      gap: var(--space-m);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.3);
      position: relative;
      overflow: hidden;
    }}
    
    .course-item::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--brand);
      border-radius: 4px 0 0 4px;
    }}
    
    .course-item:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }}
    
    .training-content {{
      flex: 1;
    }}
    
    .training-title {{
      margin: 0 0 var(--space-s) 0;
      display: flex;
      align-items: center;
      gap: var(--space-s);
      font-weight: 600;
      font-size: var(--text-l);
      color: var(--gray-800);
    }}
    
    .training-desc {{
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-600);
      font-size: var(--text-xs);
    }}
    
    .training-meta {{
      display: flex;
      gap: var(--space-s);
      font-size: var(--text-xs);
      color: var(--gray-500);
    }}
    
    .training-btn {{
      background: var(--brand);
      color: white;
      border: none;
      padding: var(--space-xs) var(--space-s);
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
      font-size: var(--text-xs);
      transition: all var(--speed);
    }}
    
    .training-btn:hover {{
      filter: brightness(.95);
      transform: translateY(-1px);
    }}
    
    .priority-critical::before {{ background: #dc3545; }}
    .priority-high::before {{ background: #fd7e14; }}
    .priority-normal::before {{ background: #28a745; }}
    .priority-low::before {{ background: #6c757d; }}
    
    .deadline-urgent {{ background: rgba(248, 215, 218, 0.3); }}
    .deadline-soon {{ background: rgba(255, 243, 205, 0.3); }}
    
    .status-badge {{ padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
    .status-active {{ background: #d4edda; color: #155724; }}
    .status-urgent {{ background: #f8d7da; color: #721c24; }}
    .status-expired {{ background: #f5c6cb; color: #721c24; }}
    

    
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: var(--space-m);
      margin: var(--space-l) 0;
    }}
    
    .modal {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: modalFadeIn 0.3s ease;
    }}
    
    .modal.show {{
      display: flex;
    }}
    
    .modal-content {{
      background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #ecfdf5 100%);
      backdrop-filter: blur(20px);
      border-radius: 20px;
      max-width: 900px;
      width: 95%;
      max-height: 85vh;
      overflow: hidden;
      box-shadow: 0 25px 80px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.5);
      border: 1px solid rgba(255, 255, 255, 0.8);
      animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    
    .modal-header {{
      padding: var(--space-xl) var(--space-xl) var(--space-l);
      background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%);
      color: white;
      position: relative;
      border-radius: 20px 20px 0 0;
    }}
    
    .modal-header h3 {{
      margin: 0;
      font-size: var(--text-xl);
      font-weight: 700;
      color: white;
    }}
    
    .modal-body {{
      padding: var(--space-xl);
      overflow-y: auto;
      max-height: calc(85vh - 120px);
    }}
    
    .modal-close {{
      position: absolute;
      top: 15px;
      right: 20px;
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
      border-radius: 50%;
      width: 40px;
      height: 40px;
      font-size: 20px;
      cursor: pointer;
      color: white;
      transition: all var(--speed);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    
    .modal-close:hover {{
      background: rgba(255, 255, 255, 0.3);
      transform: scale(1.1);
    }}
    
    @keyframes modalFadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    
    @keyframes modalSlideIn {{
      from {{ 
        opacity: 0;
        transform: translateY(-50px) scale(0.9);
      }}
      to {{ 
        opacity: 1;
        transform: translateY(0) scale(1);
      }}
    }}
    </style>
</head>
<body>
    <div class="container" style="padding-top: var(--space-m);">
        <!-- Header в виде карточки -->
        <div class="hero" style="background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%); color: white; grid-column: 1 / -1; margin: 0 0 20px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 32px;">
                    <img src="/calpoly-logo.png" alt="Cal Poly" height="32" style="filter: brightness(0) invert(1);">
                    <div>
                        <div style="font-size: 28px; font-weight: 400; color: white; letter-spacing: -0.01em;">👋 Hello, <strong onclick="showUserProfile()" style="cursor: pointer; text-decoration: underline; text-decoration-style: solid; text-decoration-thickness: 1px; text-underline-offset: 4px;">{user["name"]}</strong></div>
                        <div id="motivationalStatus" onclick="openMeditation()" style="font-size: 20px; color: rgba(255, 255, 255, 0.9); margin-top: 4px; font-weight: 300; cursor: pointer; transition: opacity 0.3s ease;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">✨ {user["role"]} | {user["department"]}</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <button id="coffeeButton" onclick="openAIChat()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); white-space: nowrap; position: relative;">
                        ☕ Random Coffee AI
                        <span id="messageNotification" style="display: none; position: absolute; top: -8px; right: -8px; background: #ef4444; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; font-weight: bold; text-align: center; line-height: 20px;"></span>
                    </button>


                    <button onclick="window.history.back()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3);">Logout</button>
                </div>
            </div>
        </div>
    
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: stretch; min-height: 400px;">
            <div class="hero" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); display: flex; flex-direction: column; justify-content: space-between; min-height: 400px;">
                <div>
                    <h1 style="font-size: 48px; font-weight: 800; margin-bottom: 30px;">🚀 My Journey</h1>
                    
                    <!-- Прогресс бар -->
                    <div style="background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); backdrop-filter: blur(10px); border-radius: 16px; padding: var(--space-l); border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 30px;">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: var(--space-s);">
                            <span style="font-weight: 600; color: var(--gray-800); font-size: var(--text-l);">Training Progress</span>
                            <span style="font-weight: 700; color: var(--brand); font-size: var(--text-l);">{round((sum(1 for a in assignments if a.get('is_completed', False)) / len(assignments) * 100) if assignments else 100)}%</span>
                        </div>
                        <div style="position: relative; height: 12px; border-radius: 999px; background: rgba(200,200,200,0.4); overflow: hidden; margin: var(--space-s) 0;">
                            <div style="height: 100%; width: {round((sum(1 for a in assignments if a.get('is_completed', False)) / len(assignments) * 100) if assignments else 100)}%; background: linear-gradient(90deg, var(--brand), var(--success)); transition: width 0.6s ease; border-radius: 999px;"></div>
                        </div>
                        <div style="display: flex; gap: var(--space-m); margin-top: var(--space-s); font-size: var(--text-xs); color: var(--gray-700);">
                            <span><strong style="color: var(--success);">{sum(1 for a in assignments if a.get('is_completed', False))}</strong> Completed</span>
                            <span><strong style="color: var(--blue);">{len(active_courses)}</strong> Active</span>
                            <span><strong style="color: var(--red);">{len(expired_courses)}</strong> Overdue</span>
                        </div>
                    </div>
                </div>
                
                <!-- Compliance Report & Safety Store Buttons -->
                <div style="text-align: center; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                    <button onclick="downloadComplianceReport()" style="background: linear-gradient(135deg, #7fb3d3 0%, #5b9bd5 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(127, 179, 211, 0.4);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(127, 179, 211, 0.5)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(127, 179, 211, 0.4)'">
                        📄 COMPLIANCE REPORT
                    </button>
                    <button onclick="openSafetyStore()" style="background: linear-gradient(145deg, #fed7aa 0%, #fdba74 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(254, 215, 170, 0.4);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(254, 215, 170, 0.5)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(254, 215, 170, 0.4)'">
                        👕 SAFE & SWAG
                    </button>

                </div>
            </div>
            
            <!-- Правая колонка - Action Required -->
            <div class="hero" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%) !important; color: white !important; border-radius: 32px !important; box-shadow: 0 20px 40px rgba(245, 158, 11, 0.3) !important; display: flex; flex-direction: column; justify-content: space-between; min-height: 400px;">
                <div>
                    <h1 style="font-size: 46px; font-weight: 800; margin-bottom: 40px;">🔔 Action Required</h1>
                    
                    <!-- Блок описания тренинга (напротив Training Progress) -->
                    <div id="nextActionContent" style="margin-bottom: 20px;">
                        <!-- Контент будет загружен через JavaScript -->
                    </div>
                </div>
                
                <!-- Кнопка START TRAINING (напротив кнопок COMPLIANCE REPORT & SAFE & SWAG) -->
                <div id="startTrainingButton" style="text-align: left; display: flex; gap: 12px; justify-content: flex-start; flex-wrap: wrap;">
                    <!-- Кнопка будет добавлена через JavaScript -->
                </div>
            </div>
        </div>
    '''
    
    # Передаем реальные данные в JavaScript
    import json
    html += f'''
        <script>
            const upcoming_deadlines = {json.dumps([dict(course) for course in upcoming_deadlines])};
            const active_courses = {json.dumps([dict(course) for course in active_courses])};
        </script>
    '''
    
    # Функция для получения эмодзи course
    def get_course_emoji(course_id):
        course_lower = course_id.lower()
        # Точные соответствия для курсов из базы
        if course_id.startswith('OSHA-'):
            return '🛡️'
        elif course_id.startswith('HAZWOPER-'):
            return '⚗️'
        elif course_id.startswith('HAZCOM-'):
            return '⚠️'
        elif course_id.startswith('PPE-'):
            return '🦺'
        elif course_id.startswith('FIRE-'):
            return '🔥'
        elif course_id.startswith('LADDER-'):
            return '🪜'
        elif course_id.startswith('ERG-'):
            return '🪑'
        elif course_id.startswith('BIOSAFETY-'):
            return '☣️'
        elif course_id.startswith('BBP-'):
            return '☣️'
        elif course_id.startswith('CHEM-SPILL-'):
            return '⚗️'
        elif course_id.startswith('LAB-SAFETY-'):
            return '🧪'
        elif course_id.startswith('RADIATION-'):
            return '☢️'
        elif course_id.startswith('LASER-'):
            return '☢️'
        elif course_id.startswith('LOTO-'):
            return '⚡'
        elif course_id.startswith('FORKLIFT-'):
            return '🚛'
        elif course_id.startswith('RESPIRATOR-'):
            return '😷'
        elif course_id.startswith('HEAT-'):
            return '🌡️'
        elif course_id.startswith('IDP-'):
            return '🦠'
        elif course_id.startswith('WASTE-') or 'DOT' in course_id:
            return '♻️'
        # Дополнительные курсы из системы
        elif course_id.startswith('RAD-SAFETY-') or course_id.startswith('RADIATION-'):
            return '☢️'
        elif course_id.startswith('POWERED-INDUSTRIAL-TRUCKS-'):
            return '🚛'
        elif course_id.startswith('BLOODBORNE-PATHOGENS') or course_id.startswith('BIOSAFETY-UNIVERSAL-'):
            return '☣️'
        elif course_id.startswith('NANO-'):
            return '🔬'
        # Дополнительные проверки по содержанию
        elif 'fire' in course_lower or 'пожар' in course_lower:
            return '🔥'
        elif 'hazwoper' in course_lower or 'hazmat' in course_lower or 'chem' in course_lower or 'spill' in course_lower:
            return '⚗️'
        elif 'biosafety' in course_lower or 'bbp' in course_lower or 'bloodborne' in course_lower:
            return '☣️'
        elif 'radiation' in course_lower or 'laser' in course_lower or 'alara' in course_lower or 'rad-safety' in course_lower:
            return '☢️'
        elif 'lab' in course_lower:
            return '🧪'
        elif 'ppe' in course_lower or 'protective' in course_lower:
            return '🦺'
        elif 'respirator' in course_lower or 'respiratory' in course_lower:
            return '😷'
        elif 'ergonomic' in course_lower or 'erg-' in course_lower:
            return '🪑'
        elif 'loto' in course_lower or 'lockout' in course_lower or 'electrical' in course_lower:
            return '⚡'
        elif 'forklift' in course_lower or 'truck' in course_lower or 'industrial-trucks' in course_lower:
            return '🚛'
        elif 'ladder' in course_lower or 'fall' in course_lower:
            return '🪜'
        elif 'waste' in course_lower or 'dot' in course_lower:
            return '♻️'
        elif 'heat' in course_lower:
            return '🌡️'
        elif 'infectious' in course_lower or 'disease' in course_lower:
            return '🦠'
        elif 'nano' in course_lower:
            return '🔬'
        elif 'osha' in course_lower:
            return '🛡️'
        else:
            return '📚'
    
    # Определяем курс, который показан в Next Action Required
    next_course_id = None
    if upcoming_deadlines:
        next_course_id = sorted(upcoming_deadlines, key=lambda x: x['days_left'])[0]['course_id']
    elif active_courses:
        priority_order = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1}
        next_course_id = sorted(active_courses, key=lambda x: priority_order.get(x['priority'], 0), reverse=True)[0]['course_id']
    
    # Срочные дедлайны (исключаем курс из Next Action Required)
    remaining_urgent = [c for c in upcoming_deadlines if c['course_id'] != next_course_id]
    if remaining_urgent:
        html += '''
        <div class="tahoe-card tahoe-animate">
            <h1 style="font-size: 48px; font-weight: 800;">⚠️ Срочные дедлайны (менее 7 дней)</h1>
        '''
        for course in remaining_urgent:
            priority_class = f"priority-{course['priority']}"
            deadline_class = "deadline-urgent" if course['days_left'] <= 3 else "deadline-soon"
            
            html += f'''
        <div class="course-item {priority_class} {deadline_class}">
            <div class="training-content">
                <h3 class="training-title">
                    <span>{get_course_emoji(course["course_id"])}</span>
                    {course["course_id"]}
                </h3>
                {f'<div style="margin-bottom: 12px; font-style: italic; color: var(--gray-600); font-size: var(--text-xs); line-height: 1.4;">💡 {course["reason"]}</div>' if course["reason"] else ''}
                <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="background: {'#dc2626' if course['priority'] == 'critical' else '#ea580c' if course['priority'] == 'high' else '#10b981' if course['priority'] == 'normal' else '#6b7280'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{course["priority"].upper()}</span>
                    <span style="font-size: 12px; font-weight: 600;">📅 Enroll: {course["assigned_date"]}</span>
                    <span style="font-size: 12px; font-weight: 600;">🏁 Due: {course["deadline_date"]}</span>
                    <span style="font-size: 12px; font-weight: 600;">⏰ {course["days_left"]} дн. осталось</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; align-items: stretch; width: 150px;">
                <button style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 20px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3); width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(16, 185, 129, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(16, 185, 129, 0.3)'" onclick="completeCourse('{course["course_id"]}')">
                    START<br>TRAINING
                </button>
            </div>
        </div>
            '''
        html += '</div>'
    
    # Активные курсы (исключаем курс из Next Action Required)
    remaining_active = [c for c in active_courses if c['course_id'] != next_course_id]
    if remaining_active:
        html += f'''
        <div class="hero" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); margin-top: 20px;">
            <h1>📚 Active Certifications</h1>
        '''
        for course in remaining_active:
            priority_class = f"priority-{course['priority']}"
            
            html += f'''
        <div class="course-item {priority_class}">
            <div class="training-content">
                <h3 class="training-title">
                    <span>{get_course_emoji(course["course_id"])}</span>
                    {course["course_id"]}
                </h3>
                {f'<div style="margin-bottom: 12px; font-style: italic; color: var(--gray-600); font-size: var(--text-xs); line-height: 1.4;">💡 {course["reason"]}</div>' if course["reason"] else ''}
                <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="background: {'#dc2626' if course['priority'] == 'critical' else '#ea580c' if course['priority'] == 'high' else '#10b981' if course['priority'] == 'normal' else '#6b7280'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{course["priority"].upper()}</span>
                    <span style="font-size: 12px; font-weight: 600;">📅 Enroll: {course["assigned_date"]}</span>
                    <span style="font-size: 12px; font-weight: 600;">🏁 Due: {course["deadline_date"]}</span>
                    <span style="font-size: 12px; font-weight: 600;">🔄 Renewal: {course["renewal_months"]} мес.</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; align-items: stretch; width: 150px;">
                <button style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 20px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3); width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(16, 185, 129, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(16, 185, 129, 0.3)'" onclick="completeCourse('{course["course_id"]}')">
                    START<br>TRAINING
                </button>
            </div>
        </div>
            '''
        html += '</div>'
    
    # Просроченные курсы
    if expired_courses:
        html += '''
        <div class="tahoe-card tahoe-animate">
            <h1 style="font-size: 48px; font-weight: 800;">❌ Просроченные курсы</h1>
        '''
        for course in expired_courses:
            priority_class = f"priority-{course['priority']}"
            
            html += f'''
        <div class="course-item {priority_class}" style="background: rgba(248, 215, 218, 0.3);">
            <div class="training-content">
                <h3 class="training-title">
                    <span>{get_course_emoji(course["course_id"])}</span>
                    {course["course_id"]}
                </h3>
                {f'<div style="margin-bottom: 12px; font-style: italic; color: var(--gray-600); font-size: var(--text-xs); line-height: 1.4;">💡 {course["reason"]}</div>' if course["reason"] else ''}
                <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="background: {'#dc2626' if course['priority'] == 'critical' else '#ea580c' if course['priority'] == 'high' else '#10b981' if course['priority'] == 'normal' else '#6b7280'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{course["priority"].upper()}</span>
                    <span style="font-size: 12px; font-weight: 600;">📅 Enroll: {course["assigned_date"]}</span>
                    <span style="font-size: 12px; font-weight: 600;">❌ Overdue: {abs(course["days_left"])} дн.</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; align-items: flex-end;">
            </div>
        </div>
            '''
        html += '</div>'
    
    # Завершенные курсы
    completed_courses = [a for a in assignments if a.get('is_completed', False)]
    if completed_courses:
        html += f'''
        <div class="hero" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); margin-top: var(--space-xl);">
            <h1>✅ Completed Certifications ({len(completed_courses)})</h1>
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
        <div class="course-item {priority_class}" style="background: rgba(212, 237, 218, 0.3);">
            <div class="training-content">
                <h3 class="training-title" style="margin: -16px 0 var(--space-s) 0;">
                    <span>{get_course_emoji(course_id)}</span>
                    {course_id}
                </h3>
                {f'<div style="margin-bottom: 12px; font-style: italic; color: var(--gray-600); font-size: var(--text-xs); line-height: 1.4;">💡 {assignment.get("reason", "")}</div>' if assignment.get("reason") else ''}
                <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; margin-bottom: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="background: {'#dc2626' if priority == 'critical' else '#ea580c' if priority == 'high' else '#10b981' if priority == 'normal' else '#6b7280'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">{priority.upper()}</span>
                    <span style="font-size: 12px; font-weight: 600;">📅 Enroll: {assigned_date}</span>
                    <span style="font-size: 12px; font-weight: 600;">✅ Completed: {completed_date}</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; align-items: stretch; width: 150px;">
                <button style="background: linear-gradient(145deg, #fed7aa 0%, #fdba74 100%); color: #1e293b; border: none; padding: 20px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 6px 20px rgba(253, 186, 116, 0.3); width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(253, 186, 116, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(253, 186, 116, 0.3)'" onclick="viewCourseInfo('{course_id}', '{completed_date}')">
                    VIEW<br>INFO
                </button>
            </div>
        </div>
            '''
        html += '</div>'
    
    # Hide "no courses" message - section removed entirely
    
    html += '''
        
        <!-- Help & Support Section -->
        <div class="hero">
            <h1 style="font-size: 48px; font-weight: 800;">📱 Help & Support</h1>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: stretch;">
                <!-- Contact EHS Office -->
                <div class="training-card">
                    <div class="training-content">
                        <h3 class="training-title">
                            <span>🏫</span>
                            Contact EHS Office
                        </h3>
                        <p class="training-desc">Environmental Health & Safety Office support</p>
                        <div style="display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap;">
                            <a href="tel:+18057566661" style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">☎️ (805) 756-6661</a>
                            <a href="mailto:ehs@calpoly.edu" style="background: #3b82f6; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">📧 ehs@calpoly.edu</a>
                        </div>
                    </div>
                </div>
                
                <!-- Follow Cal Poly -->
                <div class="training-card" style="justify-content: space-between;">
                    <div class="training-content" style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                        <h3 class="training-title">
                            <span>🌐</span>
                            Follow Cal Poly
                        </h3>
                        <p class="training-desc">Stay connected with Cal Poly on social media</p>
                        <div style="display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap;">
                            <a href="https://www.calpoly.edu" target="_blank" style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">Website</a>
                            <a href="https://instagram.com/calpoly" target="_blank" style="background: #e1306c; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">Instagram</a>
                            <a href="https://x.com/calpoly" target="_blank" style="background: #000; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">X</a>
                            <a href="https://facebook.com/calpoly" target="_blank" style="background: #1877f2; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">Facebook</a>
                            <a href="https://linkedin.com/school/cal-poly" target="_blank" style="background: #0a66c2; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">LinkedIn</a>
                            <a href="https://youtube.com/calpoly" target="_blank" style="background: #ff0000; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: 500;">YouTube</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal -->
    <div id="mainModal" class="modal" onclick="if(event.target === this) closeModal()">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modalTitle">Title</h3>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Content -->
            </div>
        </div>
    </div>

    <script>
        // Мотивирующие статусы для охраны труда
        const motivationalStatuses = [
            'Test completed? Time to relax and meditate! 🧘‍♀️',
            'You passed! Now breathe deeply and unwind! ✨',
            'Great job on the test! You deserve a peaceful moment! 🌸',
            'Training done? Perfect time for mindful meditation! 🕯️',
            'Test success! Reward yourself with inner peace! 🌟',
            'Finished the course? Your mind deserves rest now! 🍃',
            'Well done! Take a moment to center yourself! 🧘‍♂️',
            'Test passed! Time for some zen and tranquility! 🌊',
            'Achievement unlocked! Now unlock your inner calm! 🔓',
            'Course complete? Complete your day with meditation! 🌅'
        ];
        
        function getRandomMotivationalStatus() {
            const randomIndex = Math.floor(Math.random() * motivationalStatuses.length);
            return motivationalStatuses[randomIndex];
        }
        
        function updateMotivationalStatus() {
            const statusElement = document.getElementById('motivationalStatus');
            if (statusElement) {
                const status = getRandomMotivationalStatus();
                const parts = status.split(' ');
                const emoji = parts.pop();
                const text = parts.join(' ');
                statusElement.innerHTML = `<span style="text-decoration: underline; text-decoration-style: dashed; text-underline-offset: 4px; text-decoration-thickness: 1px;">${text}</span> ${emoji}`;
            }
        }
        
        // Modal functions
        function showModal(title, content) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalBody').innerHTML = content;
            document.getElementById('mainModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('mainModal').classList.remove('show');
        }
        
        // Close modal on Esc key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModal();
            }
        });
        
        function openMeditation() {
            const meditationHTML = `
                <div style="text-align: center; padding: 0;">
                    <!-- Дыхательный круг -->
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px 20px; margin-bottom: 20px; position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                        <div id="meditationTimer" style="font-size: 24px; font-weight: 200; margin: 0 0 20px 0; font-family: system-ui, -apple-system, sans-serif; color: rgba(255,255,255,0.8); letter-spacing: 0.1em; position: relative; z-index: 2;">05:00</div>
                        <div id="breathingCircle" style="width: 120px; height: 120px; border: 3px solid rgba(255,255,255,0.8); border-radius: 50%; margin: 0 auto 20px; transition: transform 4s ease-in-out; background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%); box-shadow: 0 0 40px rgba(255,255,255,0.3), inset 0 0 30px rgba(255,255,255,0.1); position: relative; z-index: 2;"></div>
                        <div id="breathingGuide" style="font-size: 20px; opacity: 0; transition: opacity 0.5s ease; color: white; font-weight: 300; margin-bottom: 12px; position: relative; z-index: 2;">Breathe...</div>
                        <div id="affirmationText" style="font-size: 14px; opacity: 0; transition: opacity 1s ease; color: rgba(255,255,255,0.7); font-weight: 300; font-style: italic; position: relative; z-index: 2; min-height: 16px;"></div>
                    </div>
                    
                    <!-- Настройки -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <div style="color: var(--gray-700); font-size: 12px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Duration</div>
                            <div style="display: flex; gap: 8px; justify-content: center;">
                                <button onclick="setMeditationTime(180)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">3m</button>
                                <button onclick="setMeditationTime(300)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">5m</button>
                                <button onclick="setMeditationTime(600)" style="background: #f0f9ff; color: #0369a1; border: 1px solid #bae6fd; padding: 8px 20px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;">10m</button>
                            </div>
                        </div>
                        <div>
                            <div style="color: var(--gray-700); font-size: 12px; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">Controls</div>
                            <div style="display: flex; gap: 8px; justify-content: center;">
                                <button onclick="startMeditation()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">▶</button>
                                <button onclick="pauseMeditation()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">⏸</button>
                                <button onclick="resetMeditation()" style="background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-size: 12px; font-weight: 600;">↻</button>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px); border-radius: 16px; padding: 16px; margin-top: 20px; border: 2px solid rgba(255, 255, 255, 0.6); box-shadow: 0 4px 16px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 14px; color: var(--gray-700); line-height: 1.4;">
                            Have you tried our low-calorie pastries at the <a href="#" style="color: var(--brand); text-decoration: underline;">cafeteria</a>?<br>
                            Get 10% off with promo code <strong style="background: rgba(14, 122, 78, 0.1); padding: 2px 6px; border-radius: 4px; color: var(--brand);">"meditation"</strong>.
                        </div>
                    </div>
                </div>
                
                <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.3; }
                    50% { transform: scale(1.1) rotate(180deg); opacity: 0.1; }
                }
                </style>
            `;
            showModal('🧘‍♀️ Mindful Meditation', meditationHTML);
        }
        

        
        function openAIChat() {
            // Сбрасываем уведомления при открытии чата
            document.getElementById('messageNotification').style.display = 'none';
            
            const coffeeChatHTML = `
                <div style="padding: 0;">
                    <div style="display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;">
                        <button onclick="showCoffeeChat()" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🤖 AI Chat</button>
                        <button onclick="showCoffeeMessages()" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600; position: relative;">
                            💬 Messages
                            <span id="unreadBadge" style="display: none; position: absolute; top: -8px; right: -8px; background: #fbbf24; color: #000; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; font-weight: bold; text-align: center; line-height: 20px;"></span>
                        </button>
                        <button onclick="showEnhancedProfile()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🎯 Smart Profile</button>
                        <button onclick="showCompatibilityCheck()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🧠 AI Matching</button>
                        <button onclick="showInsights()" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">📊 Insights</button>
                    </div>
                    <div id="coffeeContent" style="min-height: 400px;">
                        <div style="text-align: center; padding: 40px; color: #666;">☕ Choose an option above</div>
                    </div>
                </div>
            `;
            showModal('☕ Enhanced Random Coffee AI', coffeeChatHTML);
            showCoffeeChat(); // Показываем AI Chat по умолчанию
            
            // Обновляем индикаторы сообщений при открытии
            setTimeout(checkNewMessages, 100);
        }
        
        async function sendCoffeeMessage() {
            const input = document.getElementById('coffeeChatInput');
            const message = input.value.trim();
            if (!message) return;
            
            const messagesDiv = document.getElementById('coffeeChatMessages');
            
            messagesDiv.innerHTML += `<div style="margin: 8px 0; text-align: right;"><div style="background: #8b5cf6; color: white; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 80%;">👤 ${message}</div></div>`;
            
            input.value = '';
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            messagesDiv.innerHTML += `<div id="coffeeLoading" style="margin: 8px 0;"><div style="background: #e9ecef; padding: 8px 12px; border-radius: 12px; display: inline-block;">☕ Думаю...</div></div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('message', message);
                
                const response = await fetch('/coffee/chat', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                document.getElementById('coffeeLoading').remove();
                
                const botResponse = data.response.replace(/\\n/g, '<br>');
                messagesDiv.innerHTML += `<div style="margin: 8px 0;"><div style="background: white; border: 1px solid #dee2e6; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 80%;">☕ ${botResponse}</div></div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                // Показываем матчи если пользователь спросил
                if (message.toLowerCase().includes('матч') || message.toLowerCase().includes('matches')) {
                    loadUserMatches();
                }
                
                // Обновляем счетчик сообщений
                setTimeout(checkNewMessages, 1000);
                
            } catch (error) {
                document.getElementById('coffeeLoading').remove();
                messagesDiv.innerHTML += `<div style="margin: 8px 0;"><div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 8px 12px; border-radius: 12px; display: inline-block;">❌ Error: ${error.message}</div></div>`;
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }
        
        // Медитация - переменные
        let meditationTimeLeft = 300;
        let meditationInterval = null;
        let meditationRunning = false;
        let breathingInterval = null;
        let currentMeditationSound = null;
        let meditationAudioContext = null;
        let currentMeditationOscillator = null;
        
        function updateMeditationDisplay() {
            const minutes = Math.floor(meditationTimeLeft / 60);
            const seconds = meditationTimeLeft % 60;
            const timerEl = document.getElementById('meditationTimer');
            if (timerEl) {
                timerEl.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }
        }
        
        function setMeditationTime(seconds) {
            if (!meditationRunning) {
                meditationTimeLeft = seconds;
                updateMeditationDisplay();
            }
        }
        
        function startMeditation() {
            if (!meditationRunning && meditationTimeLeft > 0) {
                meditationRunning = true;
                startBreathing();
                
                meditationInterval = setInterval(() => {
                    meditationTimeLeft--;
                    updateMeditationDisplay();
                    
                    if (meditationTimeLeft <= 0) {
                        pauseMeditation();
                        alert('🎉 Медитация завершена!');
                    }
                }, 1000);
            }
        }
        
        function pauseMeditation() {
            meditationRunning = false;
            if (meditationInterval) {
                clearInterval(meditationInterval);
                meditationInterval = null;
            }
            stopBreathing();
        }
        
        function resetMeditation() {
            pauseMeditation();
            meditationTimeLeft = 300;
            updateMeditationDisplay();
        }
        
        const affirmations = [
            'You are calm and centered',
            'Peace flows through you',
            'You are exactly where you need to be',
            'Your mind is clear and focused',
            'You radiate inner strength',
            'Every breath brings you peace',
            'You are worthy of rest and relaxation',
            'Your thoughts are gentle and kind',
            'You trust in your inner wisdom',
            'You are grateful for this moment'
        ];
        
        let affirmationInterval = null;
        
        function startBreathing() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            const affirmation = document.getElementById('affirmationText');
            if (!guide || !circle) return;
            
            guide.style.opacity = '1';
            
            let breathingPhase = 0; // 0: inhale, 1: hold, 2: exhale, 3: hold
            
            breathingInterval = setInterval(() => {
                switch(breathingPhase) {
                    case 0: // Inhale
                        guide.textContent = 'Inhale...';
                        circle.style.transform = 'scale(1.5)';
                        break;
                    case 1: // Hold after inhale
                        guide.textContent = 'Hold...';
                        circle.style.transform = 'scale(1.5)';
                        break;
                    case 2: // Exhale
                        guide.textContent = 'Exhale...';
                        circle.style.transform = 'scale(1)';
                        break;
                    case 3: // Hold after exhale
                        guide.textContent = 'Hold...';
                        circle.style.transform = 'scale(1)';
                        break;
                }
                breathingPhase = (breathingPhase + 1) % 4;
            }, 3000);
            
            // Запускаем аффирмации
            if (affirmation) {
                let affirmationIndex = 0;
                affirmationInterval = setInterval(() => {
                    affirmation.style.opacity = '0';
                    setTimeout(() => {
                        affirmation.textContent = affirmations[affirmationIndex];
                        affirmation.style.opacity = '0.7';
                        affirmationIndex = (affirmationIndex + 1) % affirmations.length;
                    }, 500);
                }, 12000);
                
                // Показываем первую аффирмацию
                setTimeout(() => {
                    affirmation.textContent = affirmations[0];
                    affirmation.style.opacity = '0.7';
                }, 2000);
            }
        }
        
        function stopBreathing() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            const affirmation = document.getElementById('affirmationText');
            
            if (guide) guide.style.opacity = '0';
            if (circle) circle.style.transform = 'scale(1)';
            if (affirmation) affirmation.style.opacity = '0';
            
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
            
            if (affirmationInterval) {
                clearInterval(affirmationInterval);
                affirmationInterval = null;
            }
        }
        
        // Загружаем статистику при загрузке страницы
        async function showUserProfile() {
            showModal('👤 Профиль user', '<div style="text-align: center; padding: 40px;">👤 Загружаю профиль...</div>');
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/user/${userId}`);
                const data = await response.json();
                
                if (data.error) {
                    document.getElementById('modalBody').innerHTML = `<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ ${data.error}</div>`;
                    return;
                }
                
                const completedCount = data.assignments.filter(a => a.is_completed).length;
                const expiredCount = data.assignments.filter(a => a.is_expired && !a.is_completed).length;
                const activeCount = data.assignments.filter(a => !a.is_completed && !a.is_expired).length;
                const urgentDeadlines = data.assignments.filter(a => {
                    if (a.is_completed || a.is_expired) return false;
                    const assignedDate = new Date(a.timestamp);
                    const deadlineDays = a.deadline_days || 30;
                    const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                    const daysLeft = Math.ceil((deadlineDate - new Date()) / (1000 * 60 * 60 * 24));
                    return daysLeft <= 7 && daysLeft > 0;
                }).length;
                
                let html = '<div>';
                
                html += `<div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 24px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">`;
                html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">`;
                html += `<div><h3 style="margin: 0; color: var(--gray-800); font-size: 24px;">👤 ${data.user.name}</h3><p style="margin: 4px 0 0 0; color: var(--gray-600); font-size: 14px;">${data.user.user_id}</p></div>`;
                html += `<button onclick="editProfile('${data.user.user_id}', '${data.user.name}', '${data.user.role}', '${data.user.department}')" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 12px;">✏️ Редактировать</button>`;
                html += `</div>`;
                html += `<div id="profileForm" style="display: none; margin-bottom: 16px; padding: 16px; background: rgba(255,255,255,0.5); border-radius: 12px;">`;
                html += `<input type="text" id="editName" placeholder="Имя" style="width: 100%; padding: 8px; margin: 4px 0; border: 1px solid #ddd; border-radius: 6px;">`;
                html += `<input type="text" id="editRole" placeholder="Роль" style="width: 100%; padding: 8px; margin: 4px 0; border: 1px solid #ddd; border-radius: 6px;">`;
                html += `<input type="text" id="editDepartment" placeholder="Отдел" style="width: 100%; padding: 8px; margin: 4px 0; border: 1px solid #ddd; border-radius: 6px;">`;
                html += `<div style="margin-top: 12px;"><button onclick="saveProfile('${data.user.user_id}')" style="background: #10b981; color: white; padding: 8px 16px; border: none; border-radius: 6px; margin-right: 8px; cursor: pointer;">✅ Сохранить</button><button onclick="cancelEdit()" style="background: #6b7280; color: white; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer;">❌ Отмена</button></div>`;
                html += `</div>`;
                html += `<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">`;
                html += `<div><strong style="color: var(--gray-700);">🏢 Role:</strong><br><span id="roleDisplay" style="color: var(--gray-800);">${data.user.role}</span></div>`;
                html += `<div><strong style="color: var(--gray-700);">🏭 Department:</strong><br><span id="departmentDisplay" style="color: var(--gray-800);">${data.user.department}</span></div>`;
                html += `</div></div>`;
                
                // Только карточка бейджей
                html += `<div style="display: flex; justify-content: center; margin: 15px 0;">`;
                html += `<div style="background: rgba(139, 92, 246, 0.1); padding: 16px 24px; border-radius: 12px; text-align: center; cursor: pointer; transition: all 0.3s ease;" onclick="showProfileBadges()" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(139, 92, 246, 0.2)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none'"><strong id="badgeCount" style="font-size: 24px; color: #8b5cf6;">0</strong><br><small style="color: var(--gray-600); font-weight: 600;">🏆 Achievement Badges</small></div>`;
                html += `</div>`;
                
                // Секция бейджей
                html += `
                    <div id="badgesSection" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin: 15px 0; border: 1px solid rgba(255, 255, 255, 0.3); display: none;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h3 style="margin: 0; color: var(--gray-800);">🏆 Achievement Badges</h3>
                            <button onclick="toggleBadgesSection()" style="background: none; border: none; font-size: 20px; cursor: pointer; color: var(--gray-600);">×</button>
                        </div>
                        <div id="badgesContent">
                            <div style="text-align: center; padding: 20px; color: #666;">🏆 Loading badges...</div>
                        </div>
                    </div>
                `;
                
                html += '</div>';
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ Error loading профиля</div>';
            }
        }
        
        async function loadUserMatches() {
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/coffee/matches/${userId}`);
                const data = await response.json();
                
                const matchesList = document.getElementById('matchesList');
                if (data.matches && data.matches.length > 0) {
                    let html = '<div style="margin: 12px 0; padding: 12px; background: rgba(139, 92, 246, 0.1); border-radius: 12px;">';
                    html += '<h4 style="margin: 0 0 12px 0; color: #8b5cf6;">🎯 Твои матчи:</h4>';
                    
                    data.matches.slice(-3).forEach(match => {
                        const partnerId = match.users.find(id => id !== userId) || 'unknown';
                        const status = match.status === 'confirmed' ? '✅ Подтвержден' : '⏳ Ожидает';
                        
                        html += `<div style="background: white; padding: 12px; margin: 8px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">`;
                        html += `<div><strong>${match.id}</strong><br><small>${status} | С ${partnerId}</small></div>`;
                        html += `<button onclick="openMatchChat('${match.id}')" style="background: #8b5cf6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">💬 Чат</button>`;
                        html += `</div>`;
                    });
                    
                    html += '</div>';
                    matchesList.innerHTML = html;
                    matchesList.style.display = 'block';
                } else {
                    matchesList.style.display = 'none';
                }
            } catch (error) {
                console.error('Error loading matches:', error);
            }
        }
        
        function openMatchChat(matchId) {
            const chatHTML = `
                <div id="matchChatMessages" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 16px; padding: 16px; margin: 16px 0; height: 300px; overflow-y: auto; font-size: 14px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                    <div style="text-align: center; padding: 20px; color: #666;">💬 Загружаю сообщения...</div>
                </div>
                
                <div style="display: flex; gap: 8px; margin: 16px 0;">
                    <button onclick="sendQuickReply('${matchId}', 'Привет! 👋')" style="background: #10b981; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">👋 Привет</button>
                    <button onclick="sendQuickReply('${matchId}', 'Как насчет встречи?')" style="background: #3b82f6; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">☕ Встреча?</button>
                    <button onclick="sendQuickReply('${matchId}', 'Подтверждаю! ✅')" style="background: #8b5cf6; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 12px; cursor: pointer;">✅ ОК</button>
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px;">
                    <input type="text" id="matchChatInput" placeholder="Напиши сообщение..." style="flex: 1; padding: 12px; border: 1px solid #dee2e6; border-radius: 8px; font-size: 14px;" onkeypress="if(event.key==='Enter') sendMatchMessage('${matchId}')">
                    <button onclick="sendMatchMessage('${matchId}')" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">💬 Send</button>
                </div>
            `;
            
            showModal(`💬 Чат - ${matchId}`, chatHTML);
            loadMatchMessages(matchId);
        }
        
        async function loadMatchMessages(matchId) {
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/coffee/messages/${matchId}?user_id=${userId}`);
                const data = await response.json();
                
                console.log('Loading messages for match:', matchId, 'Data:', data);
                
                const messagesDiv = document.getElementById('matchChatMessages');
                if (data.success && data.messages && data.messages.length > 0) {
                    let html = '';
                    data.messages.forEach(msg => {
                        const isOwn = msg.sender_id === userId;
                        const isSystem = msg.sender_id === 'system';
                        const time = new Date(msg.timestamp).toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                        
                        console.log('Message:', msg.message, 'Sender:', msg.sender_id, 'IsOwn:', isOwn);
                        
                        if (isSystem) {
                            html += `<div style="text-align: center; margin: 8px 0; padding: 8px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; font-size: 12px; color: #8b5cf6;">⚙️ ${msg.message}</div>`;
                        } else {
                            const align = isOwn ? 'right' : 'left';
                            const bgColor = isOwn ? '#8b5cf6' : 'white';
                            const textColor = isOwn ? 'white' : '#333';
                            const border = isOwn ? 'none' : '1px solid #dee2e6';
                            const sender = isOwn ? 'Ты' : msg.sender_id;
                            
                            html += `<div style="margin: 8px 0; text-align: ${align};">`;
                            html += `<div style="background: ${bgColor}; color: ${textColor}; border: ${border}; padding: 8px 12px; border-radius: 12px; display: inline-block; max-width: 70%;">`;
                            html += `<strong>${sender}:</strong> ${msg.message}<br><small style="opacity: 0.7; font-size: 10px;">${time}</small>`;
                            html += `</div></div>`;
                        }
                    });
                    
                    messagesDiv.innerHTML = html;
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                } else {
                    messagesDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">💬 Начните разговор!</div>';
                }
            } catch (error) {
                console.error('Error loading messages:', error);
                document.getElementById('matchChatMessages').innerHTML = '<div style="text-align: center; padding: 20px; color: #f00;">❌ Error loading</div>';
            }
        }
        
        async function sendMatchMessage(matchId) {
            const input = document.getElementById('matchChatInput');
            const message = input.value.trim();
            if (!message) return;
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('match_id', matchId);
                formData.append('sender_id', userId);
                formData.append('message', message);
                
                const response = await fetch('/coffee/send-message', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    input.value = '';
                    loadMatchMessages(matchId);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
        
        async function sendQuickReply(matchId, message) {
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('match_id', matchId);
                formData.append('sender_id', userId);
                formData.append('message', message);
                formData.append('message_type', 'quick_reply');
                
                const response = await fetch('/coffee/send-message', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    loadMatchMessages(matchId);
                }
            } catch (error) {
                console.error('Error sending quick reply:', error);
            }
        }
        
        async function checkNewMessages() {
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/coffee/unread/${userId}`);
                const data = await response.json();
                
                // Обновляем уведомление в шапке
                const notification = document.getElementById('messageNotification');
                if (notification) {
                    if (data.success && data.unread_count > 0) {
                        notification.textContent = data.unread_count > 9 ? '9+' : data.unread_count;
                        notification.style.display = 'block';
                    } else {
                        notification.style.display = 'none';
                    }
                }
                
                // Обновляем бейдж в вкладке Messages
                const unreadBadge = document.getElementById('unreadBadge');
                const messagesButton = unreadBadge ? unreadBadge.parentElement : null;
                
                if (unreadBadge && messagesButton) {
                    // Добавляем CSS анимацию если её нет
                    if (!document.getElementById('messagePulseStyle')) {
                        const style = document.createElement('style');
                        style.id = 'messagePulseStyle';
                        style.textContent = '@keyframes messagePulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }';
                        document.head.appendChild(style);
                    }
                    
                    if (data.success && data.unread_count > 0) {
                        unreadBadge.textContent = data.unread_count > 9 ? '9+' : data.unread_count;
                        unreadBadge.style.display = 'block';
                        // Добавляем пульсацию
                        messagesButton.style.animation = 'messagePulse 2s infinite';
                        messagesButton.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.5)';
                    } else {
                        unreadBadge.style.display = 'none';
                        // Убираем пульсацию
                        messagesButton.style.animation = 'none';
                        messagesButton.style.boxShadow = 'none';
                    }
                }
                
            } catch (error) {
                console.error('Error checking messages:', error);
            }
        }
        
        window.onload = function() {
            updateMotivationalStatus();
            checkNewMessages();
            loadNextAction();
            loadUserBadges();
            // Проверяем новые сообщения каждые 10 секунд
            setInterval(checkNewMessages, 10000);
        }
        
        function getCourseEmojiJS(courseId) {
            const courseLower = courseId.toLowerCase();
            // Точные соответствия для курсов из базы
            if (courseId.startsWith('OSHA-')) return '🛡️';
            if (courseId.startsWith('HAZWOPER-')) return '⚗️';
            if (courseId.startsWith('HAZCOM-')) return '⚠️';
            if (courseId.startsWith('PPE-')) return '🦺';
            if (courseId.startsWith('FIRE-')) return '🔥';
            if (courseId.startsWith('LADDER-')) return '🪜';
            if (courseId.startsWith('ERG-')) return '🪑';
            if (courseId.startsWith('BIOSAFETY-')) return '☣️';
            if (courseId.startsWith('BBP-')) return '☣️';
            if (courseId.startsWith('CHEM-SPILL-')) return '⚗️';
            if (courseId.startsWith('LAB-SAFETY-')) return '🧪';
            if (courseId.startsWith('RADIATION-')) return '☢️';
            if (courseId.startsWith('LASER-')) return '☢️';
            if (courseId.startsWith('LOTO-')) return '⚡';
            if (courseId.startsWith('FORKLIFT-')) return '🚛';
            if (courseId.startsWith('RESPIRATOR-')) return '😷';
            if (courseId.startsWith('HEAT-')) return '🌡️';
            if (courseId.startsWith('IDP-')) return '🦠';
            if (courseId.startsWith('WASTE-') || courseId.includes('DOT')) return '♻️';
            // Дополнительные курсы из системы
            if (courseId.startsWith('RAD-SAFETY-') || courseId.startsWith('RADIATION-')) return '☢️';
            if (courseId.startsWith('POWERED-INDUSTRIAL-TRUCKS-')) return '🚛';
            if (courseId.startsWith('BLOODBORNE-PATHOGENS') || courseId.startsWith('BIOSAFETY-UNIVERSAL-')) return '☣️';
            if (courseId.startsWith('NANO-')) return '🔬';
            // Дополнительные проверки
            if (courseLower.includes('fire') || courseLower.includes('пожар')) return '🔥';
            if (courseLower.includes('hazwoper') || courseLower.includes('hazmat') || courseLower.includes('chem') || courseLower.includes('spill')) return '⚗️';
            if (courseLower.includes('biosafety') || courseLower.includes('bbp') || courseLower.includes('bloodborne')) return '☣️';
            if (courseLower.includes('radiation') || courseLower.includes('laser') || courseLower.includes('alara') || courseLower.includes('rad-safety')) return '☢️';
            if (courseLower.includes('lab')) return '🧪';
            if (courseLower.includes('ppe') || courseLower.includes('protective')) return '🦺';
            if (courseLower.includes('respirator') || courseLower.includes('respiratory')) return '😷';
            if (courseLower.includes('ergonomic') || courseLower.includes('erg-')) return '🪑';
            if (courseLower.includes('loto') || courseLower.includes('lockout') || courseLower.includes('electrical')) return '⚡';
            if (courseLower.includes('forklift') || courseLower.includes('truck') || courseLower.includes('industrial-trucks')) return '🚛';
            if (courseLower.includes('ladder') || courseLower.includes('fall')) return '🪜';
            if (courseLower.includes('waste') || courseLower.includes('dot')) return '♻️';
            if (courseLower.includes('heat')) return '🌡️';
            if (courseLower.includes('infectious') || courseLower.includes('disease')) return '🦠';
            if (courseLower.includes('nano')) return '🔬';
            if (courseLower.includes('osha')) return '🛡️';
            return '📚';
        }
        
        function loadNextAction() {
            const nextActionDiv = document.getElementById('nextActionContent');
            
            // Находим самый приоритетный курс из реальных data
            let nextCourse = null;
            
            // Приоритет: срочные дедлайны > критичные > высокие > обычные
            if (upcoming_deadlines.length > 0) {
                nextCourse = upcoming_deadlines.sort((a, b) => a.days_left - b.days_left)[0];
            } else if (active_courses.length > 0) {
                const priorityOrder = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                nextCourse = active_courses.sort((a, b) => (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0))[0];
            }
            
            if (nextCourse) {
                const isUrgent = nextCourse.days_left <= 7;
                const priorityColors = {
                    'critical': '#dc2626',
                    'high': '#ea580c', 
                    'normal': '#059669',
                    'low': '#6b7280'
                };
                
                let html = `
                    <div style="text-align: left;">
                        <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px;">
                            <div style="font-size: 64px;">${isUrgent ? '🚨' : getCourseEmojiJS(nextCourse.course_id)}</div>
                            <div>
                                <h2 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0 0 8px 0;">${nextCourse.course_id}</h2>
                                ${nextCourse.reason ? `<div style="font-size: 14px; font-style: italic; color: #374151; line-height: 1.4;">💡 ${nextCourse.reason}</div>` : ''}
                            </div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 10px;">
                            <span style="background: ${nextCourse.priority === 'critical' ? '#dc2626' : nextCourse.priority === 'high' ? '#ea580c' : nextCourse.priority === 'normal' ? '#10b981' : '#6b7280'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">${nextCourse.priority.toUpperCase()}</span>
                            <span style="font-size: 12px; font-weight: 600; color: #1f2937;">
                                ${isUrgent ? `⏰ Дедлайн через ${nextCourse.days_left} дн.` : `📅 Enroll: ${nextCourse.assigned_date}`}
                            </span>
                            <span style="font-size: 12px; font-weight: 600; color: #1f2937;">
                                🏁 Due: ${nextCourse.deadline_date}
                            </span>
                        </div>
                    </div>
                `;
                
                // Добавляем кнопку в отдельный контейнер
                const startButtonDiv = document.getElementById('startTrainingButton');
                if (startButtonDiv) {
                    startButtonDiv.innerHTML = `
                        <button onclick="completeCourse('${nextCourse.course_id}')" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(16, 185, 129, 0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px rgba(16, 185, 129, 0.3)'">
                            START TRAINING
                        </button>
                    `;
                }
                
                nextActionDiv.innerHTML = html;
            } else {
                nextActionDiv.innerHTML = `
                    <div style="text-align: left;">
                        <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px;">
                            <div style="font-size: 64px;">🎉</div>
                            <div>
                                <h2 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0 0 8px 0;">All Caught Up!</h2>
                                <div style="font-size: 14px; font-style: italic; color: #374151; line-height: 1.4;">💡 Great work! You have no active courses<br>New courses will be assigned automatically.</div>
                            </div>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 10px;">
                            <span style="background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">COMPLETED</span>
                            <span style="font-size: 12px; font-weight: 600; color: #1f2937;">
                                🌿 You've earned some time to rest and recharge
                            </span>
                        </div>
                    </div>
                `;
                
                // Добавляем кнопку Deep Breathe когда нет курсов
                const startButtonDiv = document.getElementById('startTrainingButton');
                if (startButtonDiv) {
                    startButtonDiv.innerHTML = `
                        <button onclick="openMeditation()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; cursor: pointer; font-weight: 700; font-size: 16px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(16, 185, 129, 0.4)'" onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 4px 12px rgba(16, 185, 129, 0.3)'">
                            DEEP BREATHE
                        </button>
                    `;
                }
            }
        }
        
        function editProfile(userId, name, role, department) {
            document.getElementById('profileForm').style.display = 'block';
            document.getElementById('editName').value = name;
            document.getElementById('editRole').value = role;
            document.getElementById('editDepartment').value = department;
        }
        
        function cancelEdit() {
            document.getElementById('profileForm').style.display = 'none';
        }
        
        async function saveProfile(userId) {
            const name = document.getElementById('editName').value;
            const role = document.getElementById('editRole').value;
            const department = document.getElementById('editDepartment').value;
            
            if (!name || !role || !department) {
                alert('Заполните все поля!');
                return;
            }
            
            try {
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('name', name);
                formData.append('role', role);
                formData.append('department', department);
                
                const response = await fetch('/update-profile', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    document.getElementById('profileForm').style.display = 'none';
                    document.getElementById('roleDisplay').textContent = role;
                    document.getElementById('departmentDisplay').textContent = department;
                    document.querySelector('h3').innerHTML = `👤 ${name}`;
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
                
            } catch (error) {
                console.error('Error:', error);
                alert('❌ Error сохранения');
            }
        }
        
        async function completeCourse(courseId) {
            const userId = window.location.pathname.split('/')[2];
            
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
                    // Показываем Post-Course Teaser с мерчем и бейджами
                    if (data.merch_teaser && data.merch_teaser.length > 0) {
                        showPostCourseMerchTeaser(courseId, data.merch_teaser, data.new_badges || []);
                    } else {
                        alert('✅ ' + data.message);
                        location.reload();
                    }
                } else {
                    alert('⚠️ ' + data.message);
                }
                
            } catch (error) {
                console.error('Error:', error);
                alert('❌ Error при отметке course');
            }
        }
        
        function showPostCourseMerchTeaser(courseId, merchItems, newBadges = []) {
            let html = `
                <div style="text-align: center; padding: 0;">
                    <!-- Праздничный заголовок -->
                    <div style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%); color: white; border-radius: 20px; padding: 30px 20px; margin-bottom: 20px; position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                        
                        <!-- Компактные бейджи и сертификат -->
                        <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; position: relative; z-index: 2;">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                ${newBadges.length > 0 ? `
                                    <span style="font-size: 14px; font-weight: 600; color: white;">🏆 Badges:</span>
                                    ${newBadges.map(badge => `
                                        <span style="background: rgba(255, 255, 255, 0.3); color: white; padding: 4px 8px; border-radius: 8px; font-size: 11px; font-weight: 500; display: inline-flex; align-items: center; gap: 4px;">
                                            ${badge.emoji} ${badge.name}
                                        </span>
                                    `).join('')}
                                ` : '<span style="font-size: 14px; font-weight: 600; color: white;">🎓 Course Completed!</span>'}
                            </div>
                            <button onclick="downloadCertificate('${courseId}')" style="background: rgba(255, 255, 255, 0.3); color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 12px; white-space: nowrap;">
                                📜 Certificate
                            </button>
                        </div>
                        
                        <div style="font-size: 64px; margin-bottom: 16px; position: relative; z-index: 2;">🎉</div>
                        <h2 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; position: relative; z-index: 2;">Congratulations!</h2>
                        <p style="margin: 0; font-size: 18px; opacity: 0.9; position: relative; z-index: 2;">You've completed <strong>${courseId}</strong>!</p>
                        <p style="margin: 8px 0 0 0; font-size: 16px; opacity: 0.8; position: relative; z-index: 2;">Celebrate with Cal Poly merch! 🎆</p>
                    </div>
                    </div>
                    
                    <!-- Мерч рекомендации -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
            `;
            
            merchItems.slice(0, 6).forEach(item => {
                const isExternal = item.external;
                const buyUrl = item.tracking_url || item.url || '#';
                
                html += `
                    <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 16px; border: 1px solid rgba(255, 255, 255, 0.3); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 40px rgba(0, 0, 0, 0.15)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.1)'">
                        <div style="width: 100%; height: 80px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; border-radius: 12px; overflow: hidden; background: #f8f9fa;">
                            <img src="${item.image}" alt="${item.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                        </div>
                        <h4 style="margin: 0 0 6px 0; font-size: 14px; font-weight: 600; color: var(--gray-800); text-align: center; line-height: 1.2;">${item.name}</h4>
                        <p style="margin: 0 0 8px 0; color: var(--gray-600); font-size: 12px; text-align: center; line-height: 1.3;">${item.description.substring(0, 60)}...</p>
                        <div style="text-align: center; margin-bottom: 12px;">
                            <span style="font-size: 16px; font-weight: 700; color: var(--brand);">$${item.price}</span>
                        </div>
                        <div style="display: flex; gap: 4px;">
                `;
                
                if (isExternal) {
                    html += `
                            <button onclick="trackMerchClick('${item.id}', 'buy', 'post_course'); window.open('${buyUrl}', '_blank')" style="flex: 1; background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%); color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                                🛒 Buy Now
                            </button>
                    `;
                } else {
                    html += `
                            <button onclick="trackMerchClick('${item.id}', 'customize', 'post_course'); alert('🎨 Customizer coming soon!')" style="flex: 1; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px;">
                                🎨 Custom
                            </button>
                    `;
                }
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            html += `
                    </div>
                    
                    <!-- Кнопки действий -->
                    <div style="display: flex; gap: 12px; justify-content: center; margin-top: 20px;">
                        <button onclick="openPersonalizedMerchFeed()" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">
                            🎁 Explore more
                        </button>
                    </div>
                    
                    <!-- Дисклеймер -->
                    <div style="background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(10px); border-radius: 12px; padding: 12px; margin-top: 16px; font-size: 11px; color: var(--gray-600); line-height: 1.3;">
                        ⚠️ External purchases are processed by Cal Poly Mustang Shop or Fanatics. 
                        <a href="#" style="color: var(--brand); text-decoration: underline;">Shipping & Returns</a> | 
                        <a href="#" style="color: var(--brand); text-decoration: underline;">Track Order</a>
                    </div>
                </div>
                
                <style>
                @keyframes pulse {
                    0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.3; }
                    50% { transform: scale(1.1) rotate(180deg); opacity: 0.1; }
                }
                </style>
            `;
            
            showModal('🎉 Course Completed!', html);
        }
        
        async function trackMerchClick(itemId, action, context) {
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('item_id', itemId);
                formData.append('action', action);
                formData.append('context', context);
                
                await fetch('/merch/track', {
                    method: 'POST',
                    body: formData
                });
            } catch (error) {
                console.error('Error tracking merch interaction:', error);
            }
        }
        
        async function openPersonalizedMerchFeed() {
            const userId = window.location.pathname.split('/')[2];
            
            const feedHTML = `
                <div style="padding: 0;">
                    <div id="merchFeedContent" style="min-height: 400px;">
                        <div style="text-align: center; padding: 40px; color: #666;">🎁 Loading personalized merch...</div>
                    </div>
                </div>
            `;
            
            showModal('🎁 Your Merch Feed', feedHTML);
            
            try {
                const response = await fetch(`/merch/feed/${userId}`);
                const data = await response.json();
                
                if (data.success && data.merch.length > 0) {
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px;">';
                    
                    data.merch.forEach(item => {
                        const isExternal = item.external;
                        const buyUrl = item.tracking_url || item.url || '#';
                        
                        html += `
                            <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.3);">
                                <div style="width: 100%; height: 120px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; border-radius: 12px; overflow: hidden; background: #f8f9fa;">
                                    <img src="${item.image}" alt="${item.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                                </div>
                                <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 600; color: var(--gray-800);">${item.name}</h3>
                                <p style="margin: 0 0 12px 0; color: var(--gray-600); font-size: 14px; line-height: 1.4;">${item.description}</p>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                    <span style="font-size: 18px; font-weight: 700; color: var(--brand);">$${item.price}</span>
                                    <span style="font-size: 12px; color: var(--gray-500);">Score: ${item.score}</span>
                                </div>
                                <button onclick="trackMerchClick('${item.id}', 'buy', 'personalized_feed'); window.open('${buyUrl}', '_blank')" style="width: 100%; background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%); color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease; font-size: 14px;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                                    🛒 Buy Now
                                </button>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    document.getElementById('merchFeedContent').innerHTML = html;
                } else {
                    document.getElementById('merchFeedContent').innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">🎁 No personalized merch available yet</div>';
                }
                
            } catch (error) {
                document.getElementById('merchFeedContent').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading merch feed</div>';
            }
        }
        
        async function viewCourseInfo(courseId, completedDate) {
            try {
                const userId = window.location.pathname.split('/')[2];
                
                // Получаем реальные данные из существующих эндпоинтов
                const [merchResponse, badgesResponse] = await Promise.all([
                    fetch(`/merch/feed/${userId}`).catch(() => ({ ok: false })),
                    fetch(`/badges/${userId}`).catch(() => ({ ok: false }))
                ]);
                
                let merchItems = [];
                let newBadges = [];
                
                // Получаем мерч из персонализированного фида
                if (merchResponse.ok) {
                    const merchData = await merchResponse.json();
                    if (merchData.success && merchData.merch) {
                        merchItems = merchData.merch.slice(0, 6); // Первые 6 товаров
                    }
                }
                
                // Получаем бейджи user
                if (badgesResponse.ok) {
                    const badgesData = await badgesResponse.json();
                    if (badgesData.success && badgesData.badges) {
                        newBadges = badgesData.badges.slice(-2); // Последние 2 бейджа
                    }
                }
                
                // Используем точно такой же интерфейс, как в showPostCourseMerchTeaser
                showPostCourseMerchTeaser(courseId, merchItems, newBadges);
                
            } catch (error) {
                console.error('Error loading course info:', error);
                // Fallback к обычному отображению
                const courseInfoHTML = `
                    <div style="text-align: center; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; border-radius: 16px; margin-bottom: 20px;">
                            <div style="font-size: 48px; margin-bottom: 16px;">🎓</div>
                            <h2 style="margin: 0 0 8px 0; font-size: 24px; font-weight: 700;">${courseId}</h2>
                            <div style="opacity: 0.9; font-size: 16px;">Course Completed Successfully</div>
                            <div style="opacity: 0.8; font-size: 14px; margin-top: 8px;">Completed on ${completedDate}</div>
                        </div>
                        <button onclick="downloadCertificate('${courseId}')" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; margin-right: 12px;">
                            📜 Download Certificate
                        </button>
                        <button onclick="closeModal()" style="background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer;">
                            Close
                        </button>
                    </div>
                `;
                showModal('🎓 Course Information', courseInfoHTML);
            }
        }
        
        function downloadCertificate(courseId) {
            // Симуляция скачивания сертификата
            const link = document.createElement('a');
            link.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(`Certificate of Completion\n\nCourse: ${courseId}\nCompleted: ${new Date().toLocaleDateString()}\n\nThis certifies successful completion of the safety training course.`);
            link.download = `${courseId}_Certificate.txt`;
            link.click();
            
            // Показываем уведомление
            alert('📜 Certificate downloaded successfully!');
        }
        
        // Функция генерации отчета о соответствии
        async function downloadComplianceReport() {
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/user/${userId}`);
                const data = await response.json();
                
                if (data.error) {
                    alert('❌ Error loading data user');
                    return;
                }
                
                const user = data.user;
                const assignments = data.assignments;
                const currentDate = new Date();
                
                // Анализируем статус курсов
                const completedCourses = assignments.filter(a => a.is_completed);
                const activeCourses = assignments.filter(a => !a.is_completed && !a.is_expired);
                const expiredCourses = assignments.filter(a => a.is_expired && !a.is_completed);
                const urgentDeadlines = assignments.filter(a => {
                    if (a.is_completed || a.is_expired) return false;
                    const assignedDate = new Date(a.timestamp);
                    const deadlineDays = a.deadline_days || 30;
                    const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                    const daysLeft = Math.ceil((deadlineDate - currentDate) / (1000 * 60 * 60 * 24));
                    return daysLeft <= 7 && daysLeft > 0;
                });
                
                // Определяем общий статус соответствия
                let complianceStatus = 'COMPLIANT';
                let statusColor = '#10b981';
                if (expiredCourses.length > 0) {
                    complianceStatus = 'NON-COMPLIANT';
                    statusColor = '#ef4444';
                } else if (urgentDeadlines.length > 0) {
                    complianceStatus = 'AT RISK';
                    statusColor = '#f59e0b';
                }
                
                // Генерируем отчет
                let report = `COMPLIANCE REPORT\n`;
                report += `===================\n\n`;
                report += `Employee: ${user.name} (${user.user_id})\n`;
                report += `Role: ${user.role}\n`;
                report += `Department: ${user.department}\n`;
                report += `Report Date: ${currentDate.toLocaleDateString()}\n`;
                report += `Report Time: ${currentDate.toLocaleTimeString()}\n\n`;
                
                report += `COMPLIANCE STATUS: ${complianceStatus}\n`;
                report += `Total Courses: ${assignments.length}\n`;
                report += `Completed: ${completedCourses.length}\n`;
                report += `Active: ${activeCourses.length}\n`;
                report += `Overdue: ${expiredCourses.length}\n`;
                report += `Urgent (≤7 days): ${urgentDeadlines.length}\n\n`;
                
                if (completedCourses.length > 0) {
                    report += `COMPLETED COURSES\n`;
                    report += `=================\n`;
                    completedCourses.forEach(course => {
                        const assignedDate = new Date(course.timestamp).toLocaleDateString();
                        report += `✅ ${course.course_id}\n`;
                        report += `   Assigned: ${assignedDate}\n`;
                        report += `   Priority: ${course.priority.toUpperCase()}\n`;
                        if (course.reason) report += `   Reason: ${course.reason}\n`;
                        report += `\n`;
                    });
                }
                
                if (activeCourses.length > 0) {
                    report += `ACTIVE COURSES\n`;
                    report += `==============\n`;
                    activeCourses.forEach(course => {
                        const assignedDate = new Date(course.timestamp);
                        const deadlineDays = course.deadline_days || 30;
                        const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                        const daysLeft = Math.ceil((deadlineDate - currentDate) / (1000 * 60 * 60 * 24));
                        
                        report += `📚 ${course.course_id}\n`;
                        report += `   Assigned: ${assignedDate.toLocaleDateString()}\n`;
                        report += `   Due: ${deadlineDate.toLocaleDateString()}\n`;
                        report += `   Days Left: ${daysLeft}\n`;
                        report += `   Priority: ${course.priority.toUpperCase()}\n`;
                        if (course.reason) report += `   Reason: ${course.reason}\n`;
                        report += `\n`;
                    });
                }
                
                if (urgentDeadlines.length > 0) {
                    report += `URGENT DEADLINES (≤7 DAYS)\n`;
                    report += `==========================\n`;
                    urgentDeadlines.forEach(course => {
                        const assignedDate = new Date(course.timestamp);
                        const deadlineDays = course.deadline_days || 30;
                        const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                        const daysLeft = Math.ceil((deadlineDate - currentDate) / (1000 * 60 * 60 * 24));
                        
                        report += `⚠️ ${course.course_id}\n`;
                        report += `   Due: ${deadlineDate.toLocaleDateString()}\n`;
                        report += `   Days Left: ${daysLeft}\n`;
                        report += `   Priority: ${course.priority.toUpperCase()}\n`;
                        report += `\n`;
                    });
                }
                
                if (expiredCourses.length > 0) {
                    report += `OVERDUE COURSES\n`;
                    report += `===============\n`;
                    expiredCourses.forEach(course => {
                        const assignedDate = new Date(course.timestamp);
                        const deadlineDays = course.deadline_days || 30;
                        const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                        const daysOverdue = Math.ceil((currentDate - deadlineDate) / (1000 * 60 * 60 * 24));
                        
                        report += `❌ ${course.course_id}\n`;
                        report += `   Was Due: ${deadlineDate.toLocaleDateString()}\n`;
                        report += `   Days Overdue: ${daysOverdue}\n`;
                        report += `   Priority: ${course.priority.toUpperCase()}\n`;
                        if (course.reason) report += `   Reason: ${course.reason}\n`;
                        report += `\n`;
                    });
                }
                
                report += `RECOMMENDATIONS\n`;
                report += `===============\n`;
                if (complianceStatus === 'COMPLIANT') {
                    report += `✅ Employee is fully compliant with all safety training requirements.\n`;
                    report += `✅ Continue monitoring for new course assignments.\n`;
                } else if (complianceStatus === 'AT RISK') {
                    report += `⚠️ Employee has upcoming deadlines within 7 days.\n`;
                    report += `⚠️ Immediate action required to complete urgent courses.\n`;
                } else {
                    report += `❌ Employee is non-compliant with safety training requirements.\n`;
                    report += `❌ Immediate remediation required for overdue courses.\n`;
                    report += `❌ Consider escalation to management if non-compliance persists.\n`;
                }
                
                report += `\n---\n`;
                report += `Report generated by EHS AI Mentor System\n`;
                report += `Cal Poly Environmental Health & Safety\n`;
                report += `Powered by Amazon Web Services (AWS)\n`;
                
                // Скачиваем отчет
                const blob = new Blob([report], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `Compliance_Report_${user.user_id}_${currentDate.toISOString().split('T')[0]}.txt`;
                link.click();
                window.URL.revokeObjectURL(url);
                
                // Показываем уведомление
                alert(`📄 Compliance Report downloaded successfully!\n\nStatus: ${complianceStatus}\nCompleted: ${completedCourses.length}/${assignments.length} courses`);
                
            } catch (error) {
                console.error('Error generating compliance report:', error);
                alert('❌ Error generating compliance report');
            }
        }
        
        // Функции онлайн-магазина
        async function openStore() {
            const storeHTML = `
                <div style="padding: 0;">
                    <div style="display: flex; gap: 16px; margin-bottom: 20px;">
                        <button onclick="showProducts()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">🛒 Products</button>
                        <button onclick="showCart()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">🛍️ Cart</button>
                        <button onclick="showOrders()" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">📦 Orders</button>
                    </div>
                    <div id="storeContent" style="min-height: 400px;">
                        <div style="text-align: center; padding: 40px; color: #666;">🛒 Loading store...</div>
                    </div>
                </div>
            `;
            showModal('🛒 Safety Store', storeHTML);
            showProducts();
        }
        
        async function showProducts() {
            const contentDiv = document.getElementById('storeContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">🛒 Loading products...</div>';
            
            try {
                const response = await fetch('/store/products');
                const data = await response.json();
                
                let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">';
                
                data.products.forEach(product => {
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                            <div style="font-size: 48px; text-align: center; margin-bottom: 12px;">${product.image}</div>
                            <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 600; color: var(--gray-800);">${product.name}</h3>
                            <p style="margin: 0 0 12px 0; color: var(--gray-600); font-size: 14px; line-height: 1.4;">${product.description}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                                <span style="font-size: 20px; font-weight: 700; color: var(--brand);">$${product.price}</span>
                                <span style="font-size: 12px; color: var(--gray-500);">⭐ ${product.rating} | 📦 ${product.in_stock} left</span>
                            </div>
                            <button onclick="addToCart('${product.id}')" style="width: 100%; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                                🛒 Add to Cart
                            </button>
                        </div>
                    `;
                });
                
                html += '</div>';
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading products</div>';
            }
        }
        
        async function addToCart(productId) {
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('product_id', productId);
                formData.append('quantity', '1');
                
                const response = await fetch('/store/add-to-cart', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    updateCartNotification();
                } else {
                    alert('❌ ' + data.message);
                }
                
            } catch (error) {
                alert('❌ Error adding to cart');
            }
        }
        
        async function showCart() {
            const contentDiv = document.getElementById('storeContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">🛍️ Loading cart...</div>';
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/store/cart/${userId}`);
                const data = await response.json();
                
                if (data.cart.length === 0) {
                    contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">🛍️ Your cart is empty</div>';
                    return;
                }
                
                let html = '<div>';
                
                data.cart.forEach(item => {
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid rgba(255, 255, 255, 0.3); display: flex; align-items: center; gap: 16px;">
                            <div style="font-size: 32px;">${item.product.image}</div>
                            <div style="flex: 1;">
                                <h4 style="margin: 0 0 4px 0; color: var(--gray-800);">${item.product.name}</h4>
                                <p style="margin: 0; color: var(--gray-600); font-size: 14px;">Quantity: ${item.quantity} × $${item.product.price}</p>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 18px; font-weight: 700; color: var(--brand); margin-bottom: 8px;">$${item.total_price.toFixed(2)}</div>
                                <button onclick="removeFromCart('${item.product.id}')" style="background: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px;">Remove</button>
                            </div>
                        </div>
                    `;
                });
                
                html += `
                    <div style="background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%); color: white; border-radius: 16px; padding: 20px; margin-top: 20px; text-align: center;">
                        <h3 style="margin: 0 0 16px 0;">Total: $${data.total.toFixed(2)}</h3>
                        <button onclick="showCheckout()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 16px;">
                            🚀 Checkout
                        </button>
                    </div>
                `;
                
                html += '</div>';
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading cart</div>';
            }
        }
        
        async function removeFromCart(productId) {
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('product_id', productId);
                
                const response = await fetch('/store/remove-from-cart', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ ' + data.message);
                    showCart(); // Обновляем корзину
                    updateCartNotification();
                } else {
                    alert('❌ ' + data.message);
                }
                
            } catch (error) {
                alert('❌ Error removing from cart');
            }
        }
        
        async function showCheckout() {
            const checkoutHTML = `
                <div style="padding: 20px;">
                    <h3 style="margin: 0 0 20px 0; color: var(--gray-800);">🚀 Checkout</h3>
                    <div style="margin-bottom: 16px;">
                        <label style="display: block; margin-bottom: 4px; font-weight: 600; color: var(--gray-700);">Full Name:</label>
                        <input type="text" id="shippingName" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;" placeholder="Enter your full name">
                    </div>
                    <div style="margin-bottom: 16px;">
                        <label style="display: block; margin-bottom: 4px; font-weight: 600; color: var(--gray-700);">Shipping Address:</label>
                        <textarea id="shippingAddress" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; min-height: 80px;" placeholder="Enter your shipping address"></textarea>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 4px; font-weight: 600; color: var(--gray-700);">Phone Number:</label>
                        <input type="tel" id="shippingPhone" style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;" placeholder="Enter your phone number">
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button onclick="processCheckout()" style="flex: 1; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: 600;">🚀 Place Order</button>
                        <button onclick="showCart()" style="background: #6b7280; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">← Back</button>
                    </div>
                </div>
            `;
            
            document.getElementById('storeContent').innerHTML = checkoutHTML;
        }
        
        async function processCheckout() {
            const name = document.getElementById('shippingName').value.trim();
            const address = document.getElementById('shippingAddress').value.trim();
            const phone = document.getElementById('shippingPhone').value.trim();
            
            if (!name || !address || !phone) {
                alert('❌ Please fill in all fields');
                return;
            }
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('shipping_name', name);
                formData.append('shipping_address', address);
                formData.append('shipping_phone', phone);
                
                const response = await fetch('/store/checkout', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('🎉 Order placed successfully! Order ID: ' + data.order_id);
                    showOrders();
                    updateCartNotification();
                } else {
                    alert('❌ ' + data.message);
                }
                
            } catch (error) {
                alert('❌ Error processing checkout');
            }
        }
        
        async function showOrders() {
            const contentDiv = document.getElementById('storeContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">📦 Loading orders...</div>';
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/store/orders/${userId}`);
                const data = await response.json();
                
                if (data.orders.length === 0) {
                    contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">📦 No orders yet</div>';
                    return;
                }
                
                let html = '<div>';
                
                data.orders.forEach(order => {
                    const orderDate = new Date(order.created_at).toLocaleDateString();
                    
                    html += `
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin-bottom: 16px; border: 1px solid rgba(255, 255, 255, 0.3);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                <h4 style="margin: 0; color: var(--gray-800);">📦 Order ${order.id}</h4>
                                <span style="background: ${order.status === 'pending' ? '#f59e0b' : '#10b981'}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500;">${order.status.toUpperCase()}</span>
                            </div>
                            <p style="margin: 0 0 8px 0; color: var(--gray-600); font-size: 14px;">📅 ${orderDate} | 💰 Total: $${order.total_amount.toFixed(2)}</p>
                            <p style="margin: 0 0 12px 0; color: var(--gray-600); font-size: 14px;">📍 ${order.shipping_info.address}</p>
                            <div style="margin-top: 12px;">
                                <strong style="color: var(--gray-700);">Items:</strong>
                                <div style="margin-top: 8px;">
                    `;
                    
                    order.items.forEach(item => {
                        html += `<div style="display: flex; align-items: center; gap: 8px; margin: 4px 0;"><span>${item.product.image}</span><span style="font-size: 14px;">${item.product.name} × ${item.quantity}</span></div>`;
                    });
                    
                    html += `
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                html += '</div>';
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading orders</div>';
            }
        }
        
        async function updateCartNotification() {
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/store/cart/${userId}`);
                const data = await response.json();
                
                const notification = document.getElementById('cartNotification');
                if (data.cart.length > 0) {
                    notification.textContent = data.cart.length;
                    notification.style.display = 'block';
                } else {
                    notification.style.display = 'none';
                }
                
            } catch (error) {
                console.error('Error updating cart notification:', error);
            }
        }
        
        // Safety Store functions
        async function openSafetyStore() {
            const storeHTML = `
                <div style="padding: 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr; gap: 8px; margin-bottom: 20px;">
                        <button onclick="filterProducts('all')" id="filter-all" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-align: center;">All Products</button>
                        <button onclick="filterProducts('Personal Protection')" id="filter-personal" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-align: center;">Personal Protection</button>
                        <button onclick="filterProducts('Emergency Response')" id="filter-emergency" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-align: center;">Emergency Response</button>
                        <button onclick="filterProducts('Cal Poly Apparel')" id="filter-apparel" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-align: center;">Cal Poly Apparel</button>
                        <button onclick="filterProducts('Cal Poly Accessories')" id="filter-accessories" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 11px; text-align: center;">Cal Poly Accessories</button>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 12px; background: rgba(255,255,255,0.5); border-radius: 8px;">
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span style="font-size: 14px; color: #374151; font-weight: 600;">Department:</span>
                            <select id="departmentSelect" onchange="filterByUserDepartment()" style="padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; background: white; min-width: 150px;">
                                <option value="all">All Departments</option>
                                <option value="Engineering">Engineering</option>
                                <option value="Chemistry">Chemistry</option>
                                <option value="Biology">Biology</option>
                                <option value="Physics">Physics</option>
                                <option value="Agriculture">Agriculture</option>
                                <option value="Environmental">Environmental</option>
                            </select>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <span style="font-size: 14px; color: #374151; font-weight: 600;">Sort by:</span>
                            <select id="sortSelect" onchange="sortProducts()" style="padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; background: white; min-width: 150px;">
                                <option value="name">Name A-Z</option>
                                <option value="price-low">Price: Low to High</option>
                                <option value="price-high">Price: High to Low</option>
                                <option value="rating">Rating</option>
                            </select>
                        </div>
                    </div>
                    <div id="storeContent" style="min-height: 400px;">
                        <div style="text-align: center; padding: 40px; color: #666;">🛒 Loading products...</div>
                    </div>
                </div>
            `;
            showModal('👕 Safe & Swag', storeHTML);
            loadStoreProducts();
        }
        
        let allProducts = [];
        let currentFilter = 'all';
        let currentSort = 'name';
        
        async function loadStoreProducts() {
            try {
                const response = await fetch('/store/products?t=' + Date.now());
                const data = await response.json();
                allProducts = data.products;
                sortAndDisplayProducts(allProducts);
            } catch (error) {
                document.getElementById('storeContent').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading products</div>';
            }
        }
        
        function filterProducts(department) {
            currentFilter = department;
            
            // Update button styles
            document.querySelectorAll('[id^="filter-"]').forEach(btn => {
                btn.style.background = 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)';
            });
            
            let btnId = 'filter-all';
            let btnColor = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            
            if (department === 'Personal Protection') {
                btnId = 'filter-personal';
                btnColor = 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)';
            } else if (department === 'Emergency Response') {
                btnId = 'filter-emergency';
                btnColor = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
            } else if (department === 'Cal Poly Apparel') {
                btnId = 'filter-apparel';
                btnColor = 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)';
            } else if (department === 'Cal Poly Accessories') {
                btnId = 'filter-accessories';
                btnColor = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
            }
            
            const activeBtn = document.getElementById(btnId);
            if (activeBtn) {
                activeBtn.style.background = btnColor;
            }
            
            const filteredProducts = department === 'all' ? allProducts : allProducts.filter(p => p.department === department);
            sortAndDisplayProducts(filteredProducts);
        }
        
        function filterByUserDepartment() {
            const userDept = document.getElementById('departmentSelect').value;
            
            // Reset category buttons
            document.querySelectorAll('[id^="filter-"]').forEach(btn => {
                btn.style.background = 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)';
            });
            document.getElementById('filter-all').style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            
            let filteredProducts = allProducts;
            
            if (userDept !== 'all') {
                filteredProducts = allProducts.filter(product => {
                    // Map user departments to relevant products
                    const deptMapping = {
                        'Engineering': ['Personal Protection', 'Emergency Response', 'Cal Poly Apparel'],
                        'Chemistry': ['Personal Protection', 'Emergency Response', 'Cal Poly Accessories'],
                        'Biology': ['Personal Protection', 'Emergency Response', 'Cal Poly Accessories'],
                        'Physics': ['Personal Protection', 'Cal Poly Apparel'],
                        'Agriculture': ['Personal Protection', 'Emergency Response', 'Cal Poly Apparel'],
                        'Environmental': ['Personal Protection', 'Emergency Response', 'Cal Poly Accessories']
                    };
                    
                    return deptMapping[userDept]?.includes(product.department) || false;
                });
            }
            
            sortAndDisplayProducts(filteredProducts);
        }
        
        function sortProducts() {
            const sortValue = document.getElementById('sortSelect').value;
            currentSort = sortValue;
            const filteredProducts = currentFilter === 'all' ? allProducts : allProducts.filter(p => p.department === currentFilter);
            sortAndDisplayProducts(filteredProducts);
        }
        
        function sortAndDisplayProducts(products) {
            let sortedProducts = [...products];
            
            switch(currentSort) {
                case 'name':
                    sortedProducts.sort((a, b) => a.name.localeCompare(b.name));
                    break;
                case 'price-low':
                    sortedProducts.sort((a, b) => a.price - b.price);
                    break;
                case 'price-high':
                    sortedProducts.sort((a, b) => b.price - a.price);
                    break;
                case 'rating':
                    sortedProducts.sort((a, b) => (b.rating || 0) - (a.rating || 0));
                    break;
            }
            
            displayProducts(sortedProducts);
        }
        
        function displayProducts(products) {
            const contentDiv = document.getElementById('storeContent');
            contentDiv.innerHTML = '';
            
            if (products.length === 0) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #666;">🛒 No products found</div>';
                return;
            }
            
            const container = document.createElement('div');
            container.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;';
            
            products.forEach(product => {
                const departmentColor = product.department === 'Personal Protection' ? '#3b82f6' : '#ef4444';
                
                const productCard = document.createElement('div');
                productCard.style.cssText = 'background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;';
                productCard.onmouseover = function() { this.style.transform='translateY(-4px)'; this.style.boxShadow='0 12px 40px rgba(0, 0, 0, 0.15)'; };
                productCard.onmouseout = function() { this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(0, 0, 0, 0.1)'; };
                
                productCard.innerHTML = `
                    <div style="width: 100%; height: 120px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; border-radius: 12px; overflow: hidden; background: #f8f9fa;">
                        <img src="${product.image}" alt="${product.name}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                    </div>
                    <div style="background: ${departmentColor}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; margin-bottom: 8px; display: inline-block;">${product.department}</div>
                    <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 600; color: var(--gray-800); line-height: 1.3;">${product.name}</h3>
                    <p style="margin: 0 0 12px 0; color: var(--gray-600); font-size: 13px; line-height: 1.4;">${product.description}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <span style="font-size: 18px; font-weight: 700; color: var(--brand);">$${product.price}</span>
                        <span style="font-size: 11px; color: var(--gray-500);">⭐ ${product.rating}</span>
                    </div>
                `;
                
                const buyButton = document.createElement('button');
                buyButton.style.cssText = 'width: 100%; background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%); color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease; font-size: 14px;';
                const isCreatorSpring = product.amazon_url && product.amazon_url.includes('creator-spring.com');
                buyButton.innerHTML = isCreatorSpring ? '🛒 Buy Now' : '🛒 Buy on Amazon';
                buyButton.onclick = () => window.open(product.amazon_url, '_blank');
                buyButton.onmouseover = function() { this.style.transform='translateY(-2px)'; };
                buyButton.onmouseout = function() { this.style.transform='translateY(0)'; };
                
                productCard.appendChild(buyButton);
                container.appendChild(productCard);
            });
            
            contentDiv.appendChild(container);
        }
        
        // Profile Badge System functions
        async function loadUserBadges() {
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/badges/${userId}`);
                const data = await response.json();
                
                if (data.success) {
                    const badgeCountElement = document.getElementById('badgeCount');
                    if (badgeCountElement) {
                        badgeCountElement.textContent = data.badges.length;
                    }
                }
            } catch (error) {
                console.error('Error loading badge count:', error);
            }
        }
        
        function showProfileBadges() {
            const badgesSection = document.getElementById('badgesSection');
            badgesSection.style.display = 'block';
            loadProfileBadgesContent();
        }
        
        function toggleBadgesSection() {
            const badgesSection = document.getElementById('badgesSection');
            badgesSection.style.display = 'none';
        }
        
        async function loadProfileBadgesContent() {
            const contentDiv = document.getElementById('badgesContent');
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const [badgesResponse, progressResponse] = await Promise.all([
                    fetch(`/badges/${userId}`),
                    fetch(`/badges/${userId}/progress`)
                ]);
                
                const badgesData = await badgesResponse.json();
                const progressData = await progressResponse.json();
                
                let html = '';
                
                // Полученные бейджи
                if (badgesData.success && badgesData.badges.length > 0) {
                    html += '<h4 style="margin: 0 0 12px 0; color: var(--gray-800);">✨ Earned Badges</h4>';
                    html += '<div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px;">';
                    
                    badgesData.badges.forEach(badge => {
                        html += `
                            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border-radius: 12px; padding: 12px; text-align: center; min-width: 80px; position: relative; overflow: hidden;">
                                <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                                <div style="font-size: 24px; margin-bottom: 4px; position: relative; z-index: 2;">${badge.emoji}</div>
                                <div style="font-size: 10px; font-weight: 600; position: relative; z-index: 2;">${badge.name}</div>
                                <div style="font-size: 8px; opacity: 0.8; position: relative; z-index: 2;">${new Date(badge.earned_at).toLocaleDateString()}</div>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                }
                
                // Прогресс по бейджам
                if (progressData.success) {
                    const inProgress = progressData.progress.filter(p => p.status === 'in_progress' && p.progress > 0);
                    
                    if (inProgress.length > 0) {
                        html += '<h4 style="margin: 0 0 12px 0; color: var(--gray-800);">🎯 In Progress</h4>';
                        html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">';
                        
                        inProgress.slice(0, 3).forEach(badge => {
                            html += `
                                <div style="background: rgba(245, 158, 11, 0.1); border-radius: 12px; padding: 12px;">
                                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                                        <div style="font-size: 20px; filter: grayscale(100%); opacity: 0.7;">${badge.emoji}</div>
                                        <div style="flex: 1;">
                                            <div style="font-size: 12px; font-weight: 600; color: var(--gray-800);">${badge.name}</div>
                                            <div style="font-size: 10px; color: var(--gray-600);">${badge.description}</div>
                                        </div>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                        <span style="font-size: 10px; color: var(--gray-700);">Progress</span>
                                        <span style="font-size: 10px; font-weight: 700; color: #f59e0b;">${badge.progress}%</span>
                                    </div>
                                    <div style="height: 6px; background: rgba(0,0,0,0.1); border-radius: 3px; overflow: hidden;">
                                        <div style="height: 100%; width: ${badge.progress}%; background: #f59e0b; transition: width 0.6s ease; border-radius: 3px;"></div>
                                    </div>
                                </div>
                            `;
                        });
                        
                        html += '</div>';
                    }
                }
                
                if (!html) {
                    html = `
                        <div style="text-align: center; padding: 20px;">
                            <div style="font-size: 48px; margin-bottom: 12px; opacity: 0.5;">🏆</div>
                            <div style="font-weight: 600; margin-bottom: 8px;">No Badges Yet</div>
                            <div style="font-size: 12px; color: var(--gray-600);">Complete courses to earn your first badge!</div>
                        </div>
                    `;
                }
                
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #dc3545;">❌ Error loading badges</div>';
            }
        }
        
        async function showBadges() {
            const userId = window.location.pathname.split('/')[2];
            
            const badgesHTML = `
                <div style="padding: 0;">
                    <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                        <button onclick="showEarnedBadges()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🏆 Earned</button>
                        <button onclick="showBadgeProgress()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🎯 Progress</button>
                        <button onclick="showBadgeStore()" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">🛍️ Badge Store</button>
                    </div>
                    <div id="badgesContent" style="min-height: 400px;">
                        <div style="text-align: center; padding: 40px; color: #666;">🏆 Choose an option above</div>
                    </div>
                </div>
            `;
            
            showModal('🏆 Achievement Badges', badgesHTML);
            showEarnedBadges(); // Показываем полученные бейджи по умолчанию
        }
        
        async function showEarnedBadges() {
            const contentDiv = document.getElementById('badgesContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">🏆 Loading earned badges...</div>';
            
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/badges/${userId}`);
                const data = await response.json();
                
                if (data.success && data.badges.length > 0) {
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">';
                    
                    data.badges.forEach(badge => {
                        const earnedDate = new Date(badge.earned_at).toLocaleDateString();
                        
                        html += `
                            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border-radius: 16px; padding: 20px; text-align: center; position: relative; overflow: hidden;">
                                <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                                <div style="font-size: 48px; margin-bottom: 12px; position: relative; z-index: 2;">${badge.emoji}</div>
                                <h3 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700; position: relative; z-index: 2;">${badge.name}</h3>
                                <p style="margin: 0 0 12px 0; font-size: 14px; opacity: 0.9; position: relative; z-index: 2;">${badge.description}</p>
                                <div style="font-size: 12px; opacity: 0.8; position: relative; z-index: 2;">Earned: ${earnedDate}</div>
                                ${badge.unlocks_merch && badge.unlocks_merch.length > 0 ? `<div style="margin-top: 8px; font-size: 11px; opacity: 0.8; position: relative; z-index: 2;">🔓 Unlocks ${badge.unlocks_merch.length} merch items</div>` : ''}
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    contentDiv.innerHTML = html;
                } else {
                    contentDiv.innerHTML = `
                        <div style="text-align: center; padding: 40px;">
                            <div style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;">🏆</div>
                            <h3>No Badges Yet</h3>
                            <p>Complete courses and participate in Random Coffee to earn badges!</p>
                            <button onclick="showBadgeProgress()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 16px 32px; border-radius: 8px; cursor: pointer; font-weight: 600;">🎯 View Progress</button>
                        </div>
                    `;
                }
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading badges</div>';
            }
        }
        
        async function showBadgeProgress() {
            const contentDiv = document.getElementById('badgesContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">🎯 Loading badge progress...</div>';
            
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/badges/${userId}/progress`);
                const data = await response.json();
                
                if (data.success) {
                    let html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px;">';
                    
                    data.progress.forEach(badge => {
                        const isEarned = badge.status === 'earned';
                        const progressColor = isEarned ? '#10b981' : '#f59e0b';
                        
                        html += `
                            <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.3);">
                                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                                    <div style="font-size: 32px; ${isEarned ? '' : 'filter: grayscale(100%); opacity: 0.5;'}">${badge.emoji}</div>
                                    <div style="flex: 1;">
                                        <h4 style="margin: 0 0 4px 0; font-size: 16px; font-weight: 600; color: var(--gray-800);">${badge.name}</h4>
                                        <p style="margin: 0; font-size: 12px; color: var(--gray-600);">${badge.description || ''}</p>
                                    </div>
                                </div>
                                
                                <div style="margin-bottom: 12px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                                        <span style="font-size: 12px; font-weight: 600; color: var(--gray-700);">Progress</span>
                                        <span style="font-size: 12px; font-weight: 700; color: ${progressColor};">${badge.progress}%</span>
                                    </div>
                                    <div style="height: 8px; background: rgba(0,0,0,0.1); border-radius: 4px; overflow: hidden;">
                                        <div style="height: 100%; width: ${badge.progress}%; background: ${progressColor}; transition: width 0.6s ease; border-radius: 4px;"></div>
                                    </div>
                                </div>
                                
                                ${badge.unlocks_merch && badge.unlocks_merch.length > 0 ? `
                                <div style="background: rgba(139, 92, 246, 0.1); padding: 8px; border-radius: 8px; font-size: 11px; color: var(--gray-600);">
                                    🔓 Unlocks: ${badge.unlocks_merch.join(', ')}
                                </div>
                                ` : ''}
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                    contentDiv.innerHTML = html;
                } else {
                    contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading progress</div>';
                }
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading progress</div>';
            }
        }
        
        async function showBadgeStore() {
            const contentDiv = document.getElementById('badgesContent');
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/badges/${userId}/unlocked-merch`);
                const data = await response.json();
                
                let html = `
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h3 style="margin: 0 0 8px 0; color: var(--gray-800);">🔓 Badge-Exclusive Merch</h3>
                        <p style="margin: 0; color: var(--gray-600); font-size: 14px;">Exclusive items unlocked by your achievements!</p>
                    </div>
                `;
                
                if (data.success && data.unlocked_merch.length > 0) {
                    html += `
                        <div style="background: rgba(139, 92, 246, 0.1); padding: 16px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
                            <div style="font-size: 32px; margin-bottom: 8px;">🎉</div>
                            <div style="font-weight: 600; color: #8b5cf6;">You've unlocked ${data.unlocked_merch.length} exclusive items!</div>
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
                    `;
                    
                    // Здесь можно добавить отображение разблокированных товаров
                    data.unlocked_merch.forEach(merchId => {
                        html += `
                            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border-radius: 16px; padding: 16px; text-align: center;">
                                <div style="font-size: 32px; margin-bottom: 8px;">🏆</div>
                                <h4 style="margin: 0 0 8px 0; font-size: 14px; font-weight: 600;">${merchId}</h4>
                                <div style="font-size: 11px; opacity: 0.8;">Badge-Exclusive</div>
                                <button onclick="alert('Coming soon!')" style="width: 100%; background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; margin-top: 8px;">
                                    🛍️ View Item
                                </button>
                            </div>
                        `;
                    });
                    
                    html += '</div>';
                } else {
                    html += `
                        <div style="text-align: center; padding: 40px;">
                            <div style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;">🔒</div>
                            <h3>No Exclusive Items Yet</h3>
                            <p>Earn badges to unlock exclusive merch!</p>
                            <button onclick="showBadgeProgress()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 16px 32px; border-radius: 8px; cursor: pointer; font-weight: 600;">🎯 View Progress</button>
                        </div>
                    `;
                }
                
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading badge store</div>';
            }
        }
        
        // Enhanced Coffee Messages functions
        async function showCoffeeMessages() {
            const contentDiv = document.getElementById('coffeeContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">💬 Loading messages...</div>';
            
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/coffee/matches/${userId}`);
                const data = await response.json();
                
                let html = '';
                
                if (data.matches && data.matches.length > 0) {
                    html = `
                        <div style="display: flex; height: 400px; border-radius: 12px; overflow: hidden; background: rgba(255, 255, 255, 0.1);">
                            <!-- Список чатов -->
                            <div id="chatList" style="width: 200px; background: rgba(255, 255, 255, 0.2); border-right: 1px solid rgba(255, 255, 255, 0.3); overflow-y: auto;">
                                <div style="padding: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.2); font-weight: 600; color: var(--gray-800);">💬 Chats</div>
                    `;
                    
                    data.matches.forEach((match, index) => {
                        const partnerId = match.users.find(id => id !== userId) || 'unknown';
                        const isActive = index === 0;
                        
                        html += `
                            <div onclick="selectChat('${match.id}', '${partnerId}', this)" 
                                 style="padding: 12px 16px; cursor: pointer; border-bottom: 1px solid rgba(255, 255, 255, 0.1); transition: all 0.2s; ${isActive ? 'background: rgba(139, 92, 246, 0.2);' : ''}" 
                                 onmouseover="this.style.background='rgba(139, 92, 246, 0.1)'" 
                                 onmouseout="this.style.background='${isActive ? 'rgba(139, 92, 246, 0.2)' : 'transparent'}'">
                                <div style="font-weight: 600; font-size: 14px; color: var(--gray-800); margin-bottom: 2px;">${partnerId}</div>
                                <div style="font-size: 12px; color: var(--gray-600);">${match.id}</div>
                                <div style="font-size: 11px; color: var(--gray-500); margin-top: 2px;">${match.status === 'confirmed' ? '✅ Active' : '⏳ Pending'}</div>
                            </div>
                        `;
                    });
                    
                    html += `
                            </div>
                            
                            <!-- Окно чата -->
                            <div style="flex: 1; display: flex; flex-direction: column;">
                                <div id="chatHeader" style="padding: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.2); background: rgba(255, 255, 255, 0.1); font-weight: 600; color: var(--gray-800);">
                                    Select a chat
                                </div>
                                <div id="chatMessages" style="flex: 1; padding: 16px; overflow-y: auto; background: rgba(255, 255, 255, 0.05);">
                                    <div style="text-align: center; color: var(--gray-600); margin-top: 50px;">💬 Select a chat to start messaging</div>
                                </div>
                                <div id="chatInput" style="padding: 16px; border-top: 1px solid rgba(255, 255, 255, 0.2); background: rgba(255, 255, 255, 0.1); display: none;">
                                    <div style="display: flex; gap: 8px;">
                                        <input type="text" id="messageInput" placeholder="Type a message..." style="flex: 1; padding: 8px 12px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 20px; background: rgba(255, 255, 255, 0.8); font-size: 14px;" onkeypress="if(event.key==='Enter') sendChatMessage()">
                                        <button onclick="sendChatMessage()" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600; font-size: 14px;">💬 Send</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    contentDiv.innerHTML = html;
                    
                    // Автоматически выбираем первый чат
                    if (data.matches.length > 0) {
                        const firstMatch = data.matches[0];
                        const firstPartnerId = firstMatch.users.find(id => id !== userId) || 'unknown';
                        selectChat(firstMatch.id, firstPartnerId, document.querySelector('#chatList > div:nth-child(2)'));
                    }
                    
                } else {
                    html = `
                        <div style="text-align: center; padding: 40px;">
                            <div style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;">💬</div>
                            <h3>No Messages Yet</h3>
                            <p>Create AI matches to start conversations!</p>
                            <button onclick="showCompatibilityCheck()" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 16px 32px; border-radius: 8px; cursor: pointer; font-weight: 600;">🧠 Create Matches</button>
                        </div>
                    `;
                    contentDiv.innerHTML = html;
                }
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading messages</div>';
            }
        }
        
        let currentChatId = null;
        let currentPartnerId = null;
        
        async function selectChat(matchId, partnerId, element) {
            // Обновляем визуальное выделение
            document.querySelectorAll('#chatList > div').forEach(div => {
                if (div.onclick) div.style.background = 'transparent';
            });
            if (element) element.style.background = 'rgba(139, 92, 246, 0.2)';
            
            currentChatId = matchId;
            currentPartnerId = partnerId;
            
            // Обновляем заголовок с кликабельным именем
            document.getElementById('chatHeader').innerHTML = `💬 Chat with <span onclick="showPartnerProfile('${partnerId}')" style="cursor: pointer; text-decoration: underline; color: #8b5cf6; font-weight: 600;">${partnerId}</span>`;
            
            // Показываем поле ввода
            document.getElementById('chatInput').style.display = 'block';
            
            // Загружаем сообщения
            await loadChatMessages(matchId);
        }
        
        async function loadChatMessages(matchId) {
            const messagesDiv = document.getElementById('chatMessages');
            messagesDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">💬 Loading messages...</div>';
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const response = await fetch(`/coffee/messages/${matchId}?user_id=${userId}`);
                const data = await response.json();
                
                if (data.success && data.messages && data.messages.length > 0) {
                    let html = '';
                    data.messages.forEach(msg => {
                        const isOwn = msg.sender_id === userId;
                        const isSystem = msg.sender_id === 'system';
                        const time = new Date(msg.timestamp).toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'});
                        
                        if (isSystem) {
                            html += `<div style="text-align: center; margin: 16px 0; padding: 8px; background: rgba(139, 92, 246, 0.1); border-radius: 12px; font-size: 12px; color: #8b5cf6;">⚙️ ${msg.message}</div>`;
                        } else {
                            const align = isOwn ? 'flex-end' : 'flex-start';
                            const bgColor = isOwn ? 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)' : 'rgba(255, 255, 255, 0.8)';
                            const textColor = isOwn ? 'white' : '#333';
                            
                            html += `
                                <div style="display: flex; justify-content: ${align}; margin: 8px 0;">
                                    <div style="max-width: 70%; background: ${bgColor}; color: ${textColor}; padding: 8px 12px; border-radius: 16px; font-size: 14px; line-height: 1.4;">
                                        <div>${msg.message}</div>
                                        <div style="font-size: 11px; opacity: 0.7; margin-top: 4px;">${time}</div>
                                    </div>
                                </div>
                            `;
                        }
                    });
                    
                    messagesDiv.innerHTML = html;
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                } else {
                    messagesDiv.innerHTML = `
                        <div style="text-align: center; padding: 40px; color: var(--gray-600);">
                            <div style="font-size: 32px; margin-bottom: 12px;">👋</div>
                            <div>Start the conversation!</div>
                            <div style="font-size: 12px; margin-top: 8px; opacity: 0.7;">Say hello to ${currentPartnerId}</div>
                        </div>
                    `;
                }
                
            } catch (error) {
                messagesDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #dc3545;">❌ Error loading messages</div>';
            }
        }
        
        async function sendChatMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message || !currentChatId) return;
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('match_id', currentChatId);
                formData.append('sender_id', userId);
                formData.append('message', message);
                
                const response = await fetch('/coffee/send-message', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    input.value = '';
                    await loadChatMessages(currentChatId);
                }
            } catch (error) {
                console.error('Error sending message:', error);
            }
        }
        
        async function showPartnerProfile(partnerId) {
            try {
                const [userResponse, profileResponse] = await Promise.all([
                    fetch(`/user/${partnerId}`),
                    fetch(`/enhanced-coffee/profile/${partnerId}`)
                ]);
                
                const userData = await userResponse.json();
                const profileData = await profileResponse.json();
                
                if (userData.error) {
                    alert('❌ Профиль не найден');
                    return;
                }
                
                const user = userData.user;
                const smartProfile = profileData.success ? profileData.profile : null;
                const completedCount = userData.assignments.filter(a => a.is_completed).length;
                const activeCount = userData.assignments.filter(a => !a.is_completed && !a.is_expired).length;
                
                let profileHTML = `
                    <div style="text-align: center; padding: 0;">
                        <!-- Аватар и основная инфо -->
                        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border-radius: 16px; padding: 30px; margin-bottom: 20px; position: relative; overflow: hidden;">
                            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%); animation: pulse 4s ease-in-out infinite;"></div>
                            <div style="font-size: 64px; margin-bottom: 16px; position: relative; z-index: 2;">👤</div>
                            <h2 style="margin: 0 0 8px 0; font-size: 24px; font-weight: 700; position: relative; z-index: 2;">${user.name}</h2>
                            <div style="font-size: 14px; opacity: 0.9; position: relative; z-index: 2;">${user.user_id}</div>
                        </div>
                        
                        <!-- Информация о работе -->
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.3);">
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                                <div style="text-align: left;">
                                    <strong style="color: var(--gray-700); font-size: 12px; text-transform: uppercase;">🏢 Role:</strong><br>
                                    <span style="color: var(--gray-800); font-size: 16px; font-weight: 600;">${user.role}</span>
                                </div>
                                <div style="text-align: left;">
                                    <strong style="color: var(--gray-700); font-size: 12px; text-transform: uppercase;">🏢 Department:</strong><br>
                                    <span style="color: var(--gray-800); font-size: 16px; font-weight: 600;">${user.department}</span>
                                </div>
                            </div>
                        </div>
                `;
                
                // Добавляем Smart Profile информацию если есть
                if (smartProfile) {
                    profileHTML += `
                        <!-- Smart Profile данные -->
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.3);">
                            <h3 style="margin: 0 0 16px 0; color: var(--gray-800); font-size: 16px;">🎯 Smart Profile</h3>
                    `;
                    
                    if (smartProfile.interests && smartProfile.interests.length > 0) {
                        profileHTML += `
                            <div style="margin-bottom: 12px;">
                                <strong style="color: var(--gray-700); font-size: 12px; text-transform: uppercase;">🎯 Interests:</strong><br>
                                <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 6px;">
                        `;
                        
                        smartProfile.interests.forEach(interest => {
                            const interestColors = {
                                'lab-safety': '#dc2626',
                                'ergonomics': '#7c3aed',
                                'mental-health': '#059669',
                                'environmental': '#16a34a',
                                'emergency': '#ea580c',
                                'sports': '#2563eb',
                                'hobbies': '#db2777',
                                'learning': '#0891b2'
                            };
                            const color = interestColors[interest] || '#6b7280';
                            
                            profileHTML += `<span style="background: ${color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">${interest}</span>`;
                        });
                        
                        profileHTML += `</div></div>`;
                    }
                    
                    if (smartProfile.personality_traits && smartProfile.personality_traits.length > 0) {
                        profileHTML += `
                            <div style="margin-bottom: 12px;">
                                <strong style="color: var(--gray-700); font-size: 12px; text-transform: uppercase;">🧠 Personality:</strong><br>
                                <div style="color: var(--gray-800); font-size: 14px; margin-top: 4px;">${smartProfile.personality_traits.join(', ')}</div>
                            </div>
                        `;
                    }
                    
                    if (smartProfile.meeting_preferences) {
                        const prefs = smartProfile.meeting_preferences;
                        profileHTML += `
                            <div style="margin-bottom: 12px;">
                                <strong style="color: var(--gray-700); font-size: 12px; text-transform: uppercase;">☕ Meeting Style:</strong><br>
                                <div style="color: var(--gray-800); font-size: 14px; margin-top: 4px;">${prefs.meeting_style || 'casual'} • ${prefs.group_size || 'pair'}</div>
                            </div>
                        `;
                    }
                    
                    profileHTML += `</div>`;
                }
                
                profileHTML += `
                    </div>
                `;
                
                showModal(`👤 ${user.name}'s Profile`, profileHTML);
                
            } catch (error) {
                console.error('Error loading partner profile:', error);
                alert('❌ Error loading профиля');
            }
        }
        
        async function sendQuickMessage(message) {
            if (!currentChatId) return;
            
            try {
                const userId = window.location.pathname.split('/')[2];
                const formData = new FormData();
                formData.append('match_id', currentChatId);
                formData.append('sender_id', userId);
                formData.append('message', message);
                formData.append('message_type', 'quick_message');
                
                const response = await fetch('/coffee/send-message', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    closeModal();
                    await loadChatMessages(currentChatId);
                }
            } catch (error) {
                console.error('Error sending quick message:', error);
            }
        }
        
        // Enhanced Coffee functions
        function showCoffeeChat() {
            const contentDiv = document.getElementById('coffeeContent');
            contentDiv.innerHTML = `
                <div id="coffeeChatMessages" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 16px; padding: 16px; margin: 16px 0; height: 350px; overflow-y: auto; font-size: 14px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">
                    <div style="color: #2c3e50; text-align: left; padding: 30px 20px; font-size: 14px; line-height: 1.5;">
                        <div style="text-align: center; font-size: 48px; margin-bottom: 16px;">☕</div>
                        <div style="text-align: center; font-weight: 600; margin-bottom: 16px; color: #8b5cf6; font-size: 18px;">Enhanced Random Coffee AI</div>
                        
                        <div style="background: rgba(139, 92, 246, 0.1); padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                            <div style="font-weight: 600; margin-bottom: 8px; color: #8b5cf6;">🤖 Что я умею:</div>
                            <div style="margin-bottom: 8px;">• 🛡️ <strong>Консультации по технике безопасности</strong> — спрашивай о протоколах, courseх, требованиях</div>
                            <div style="margin-bottom: 8px;">• ☕ <strong>Поиск коллег для общения</strong> — если скучно говорить о безопасности, найду тебе друга!</div>
                            <div>• 🎯 <strong>AI-матчинг</strong> — умный подбор по интересам и совместимости</div>
                        </div>
                        
                        <div style="background: rgba(16, 185, 129, 0.1); padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                            <div style="font-weight: 600; margin-bottom: 8px; color: #10b981;">💬 Как со мной общаться:</div>
                            <div style="margin-bottom: 6px;">• Просто пиши — я отвечу на любые вопросы</div>
                            <div style="margin-bottom: 6px;">• Скажи "найти друга" — создам профиль и подберу собеседника</div>
                            <div style="margin-bottom: 6px;">• Напиши "мои матчи" — покажу твои пары для общения</div>
                            <div>• Команда "помощь" — покажу все возможности</div>
                        </div>
                        
                        <div style="text-align: center; font-size: 13px; color: #666; font-style: italic;">Начни с любого вопроса или скажи "привет"! 🚀</div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 8px; margin-top: 16px;">
                    <input type="text" id="coffeeChatInput" placeholder="Напиши что-нибудь..." style="flex: 1; padding: 12px; border: 1px solid #dee2e6; border-radius: 8px; font-size: 14px;" onkeypress="if(event.key==='Enter') sendCoffeeMessage()">
                    <button onclick="sendCoffeeMessage()" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">☕ Send</button>
                </div>
            `;
        }
        
        async function showEnhancedProfile() {
            const contentDiv = document.getElementById('coffeeContent');
            contentDiv.innerHTML = '<div style="text-align: center; padding: 40px;">🎯 Loading smart profile...</div>';
            
            const userId = window.location.pathname.split('/')[2];
            
            try {
                const response = await fetch(`/enhanced-coffee/profile/${userId}`);
                const data = await response.json();
                
                let html = '';
                
                if (data.success && data.profile) {
                    const profile = data.profile;
                    html = `
                        <div style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.3);">
                            <h3 style="margin: 0 0 16px 0; color: var(--gray-800);">🎯 Smart Profile</h3>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                                <div><strong>Interests:</strong><br>${profile.interests.join(', ')}</div>
                                <div><strong>Language:</strong><br>${profile.language}</div>
                            </div>
                            <div style="margin-bottom: 16px;"><strong>Personality Traits:</strong><br>${profile.personality_traits.join(', ') || 'Not set'}</div>
                            <div style="margin-bottom: 16px;"><strong>Meeting Preferences:</strong><br>Group: ${profile.meeting_preferences.group_size}, Style: ${profile.meeting_preferences.meeting_style}</div>
                            <div style="margin-bottom: 16px;"><strong>Total Matches:</strong> ${profile.match_history.length}</div>
                            <button onclick="showProfileEditor()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: 600;">✏️ Edit Profile</button>
                        </div>
                    `;
                } else {
                    html = `
                        <div style="text-align: center; padding: 40px;">
                            <div style="font-size: 48px; margin-bottom: 16px;">🎯</div>
                            <h3>Create Your Smart Profile</h3>
                            <p>Set up AI-powered matching with personality traits and preferences!</p>
                            <button onclick="showProfileEditor()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 16px 32px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 16px;">🚀 Create Profile</button>
                        </div>
                    `;
                }
                
                contentDiv.innerHTML = html;
                
            } catch (error) {
                contentDiv.innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading profile</div>';
            }
        }
    </script>
    
    <script src="/enhanced_coffee_ui.js"></script>

    <!-- Footer -->
    <footer style="background: linear-gradient(135deg, #1f2937 0%, #374151 100%); color: white; padding: 40px 0; margin-top: 60px; border-radius: 20px 20px 0 0;">
        <div class="container">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px; margin-bottom: 30px;">
                <!-- AI Safety Assistant -->
                <div>
                    <h4 style="color: #f97316; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">🤖 AI Safety Assistant</h4>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 14px; opacity: 0.9;">Powered By</span>
                        <img src="/AWS_2007_logo_white.png" alt="AWS" style="height: 28px;">
                    </div>
                </div>
                
                <!-- AI Matchmakers Team -->
                <div>
                    <h4 style="color: #3b82f6; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">👥 AI Matchmakers Team</h4>
                    <div style="font-size: 14px; line-height: 1.6; opacity: 0.9;">
                        <a href="https://www.sergey-ulyanov.pro/" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 600;">Sergey Ulyanov</a><br>
                        <span style="opacity: 0.7;">× Visual Studio Code × Copilot × ChatGPT</span>
                    </div>
                </div>
                
                <!-- Digital Transformation Hub -->
                <div>
                    <h4 style="color: #8b5cf6; margin: 0 0 15px 0; font-size: 18px; font-weight: 700;">🚀 Digital Transformation Hub</h4>
                    <div style="font-size: 14px; line-height: 1.6; opacity: 0.9;">
                        <span style="color: #a78bfa;">DxHub × Amazon Web Services (AWS)</span><br>
                        <span style="opacity: 0.7;">August-September 2025</span>
                    </div>
                </div>
            </div>
            
            <!-- Contact Info -->
            <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 20px; text-align: center;">
                <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 14px; opacity: 0.8;">
                    <a href="mailto:ulyanoow@gmail.com" style="color: #60a5fa; text-decoration: none; display: flex; align-items: center; gap: 5px;">📧 ulyanoow@gmail.com</a>
                    <a href="tel:+13107137738" style="color: #60a5fa; text-decoration: none; display: flex; align-items: center; gap: 5px;">📱 (310) 713-7738</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>
    '''
    
    return html