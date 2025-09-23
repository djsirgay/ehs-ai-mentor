from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from ai_mentor import AIMentor
from pdf_processor import extract_text_from_pdf
from document_tracker import DocumentTracker
from course_scheduler import CourseScheduler
from audit_logger import AuditLogger
from user_dashboard import generate_user_dashboard_html
from course_completion import CourseCompletion

app = FastAPI(title="EHS AI Mentor", version="1.0.0")
mentor = AIMentor()
doc_tracker = DocumentTracker()
scheduler = CourseScheduler()
audit_logger = AuditLogger()
course_completion = CourseCompletion()

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Только PDF файлы")
        
        pdf_bytes = await file.read()
        protocol_text = extract_text_from_pdf(pdf_bytes)
        
        # Проверяем, обрабатывался ли документ ранее
        is_duplicate, prev_info = doc_tracker.is_duplicate(protocol_text)
        
        if is_duplicate:
            return {
                "is_duplicate": True,
                "message": "Этот документ уже обрабатывался",
                "previous_processing": prev_info,
                "extracted_text": protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
            }
        
        # Обрабатываем новый документ с проверкой истории и сроков
        mentor._scheduler = scheduler  # Передаем планировщик
        result = mentor.analyze_for_all_users_with_history(protocol_text, doc_tracker)
        
        # Сохраняем информацию о обработке с пропущенными
        doc_hash = doc_tracker.save_document(protocol_text, result.get("assignments", []), result.get("skipped_duplicates", []))
        
        # Логируем обработку документа
        audit_logger.log_document_processed(
            doc_hash, 
            len(result.get("assignments", [])),
            protocol_text[:100] + "..."
        )
        
        # Логируем каждое назначение с хэшем документа
        for assignment in result.get("assignments", []):
            for course_id in assignment["courses_assigned"]:
                clean_course_id = course_id.replace(" (обновление)", "")
                priority = "normal"
                if assignment.get("course_periods"):
                    for period in assignment["course_periods"]:
                        if period["course_id"] == clean_course_id:
                            priority = period.get("priority", "normal")
                            break
                
                # Добавляем хэш документа в лог
                log_entry = {
                    "timestamp": audit_logger.logs[-1]["timestamp"] if audit_logger.logs else "2025-01-01T00:00:00",
                    "action": "course_assigned",
                    "user_id": assignment["user_id"],
                    "course_id": clean_course_id,
                    "assigned_by": "AI",
                    "reason": assignment.get("reason", ""),
                    "priority": priority,
                    "document_hash": doc_hash,
                    "id": len(audit_logger.logs) + 1
                }
                audit_logger.logs.append(log_entry)
        
        # Сохраняем логи
        audit_logger.save_logs()
        
        result["extracted_text"] = protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
        result["is_duplicate"] = False
        result["document_hash"] = doc_hash
        
        # Добавляем информацию об истекающих курсах
        expired_courses = scheduler.get_expired_courses(doc_tracker)
        result["expired_courses"] = expired_courses
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>EHS AI Mentor</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        button { background: #007bff; color: white; cursor: pointer; font-size: 16px; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; border-left: 4px solid #28a745; }
        .course { background: #e7f3ff; padding: 4px 8px; margin: 2px; border-radius: 3px; display: inline-block; }
        .assignment { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ EHS AI Mentor</h1>
        
        <div id="statsBlocks" style="display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap;">
            <div class="stat-block" onclick="showUsers()" style="background: #e3f2fd; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #1976d2;" id="userCount">-</div>
                <div style="font-size: 12px; color: #666;">👥 Пользователей</div>
            </div>
            <div class="stat-block" onclick="showCourses()" style="background: #f3e5f5; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #7b1fa2;" id="courseCount">-</div>
                <div style="font-size: 12px; color: #666;">📚 Курсов</div>
            </div>
            <div class="stat-block" onclick="showAssignments()" style="background: #e8f5e8; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #388e3c;" id="assignmentCount">-</div>
                <div style="font-size: 12px; color: #666;">🎯 Назначений</div>
            </div>
            <div class="stat-block" onclick="showDocuments()" style="background: #fff3e0; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #f57c00;" id="documentCount">-</div>
                <div style="font-size: 12px; color: #666;">📄 Документов</div>
            </div>
            <div class="stat-block" onclick="showCompletions()" style="background: #e8f5e8; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #28a745;" id="completionCount">-</div>
                <div style="font-size: 12px; color: #666;">✅ Завершено</div>
            </div>
            <div class="stat-block" onclick="showExpired()" style="background: #f8d7da; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #dc3545;" id="expiredCount">-</div>
                <div style="font-size: 12px; color: #666;">❌ Просрочено</div>
            </div>
            <div class="stat-block" onclick="showCritical()" style="background: #fff3cd; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #fd7e14;" id="criticalCount">-</div>
                <div style="font-size: 12px; color: #666;">🔴 Критичных</div>
            </div>
            <div class="stat-block" onclick="showActive()" style="background: #d1ecf1; padding: 15px; border-radius: 8px; text-align: center; min-width: 120px; flex: 1; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="font-size: 24px; font-weight: bold; color: #17a2b8;" id="activeCount">-</div>
                <div style="font-size: 12px; color: #666;">⚙️ Активных</div>
            </div>
        </div>
        <p><strong>AI анализирует протокол и назначает курсы нужным пользователям</strong></p>
        
        <div style="margin: 20px 0; padding: 20px; background: #fff; border-radius: 5px; border: 2px dashed #ddd;">
            <label><strong>Загрузите PDF файл с протоколом:</strong></label><br>
            <p>⚡ Обрабатываю первых 10 пользователей для демонстрации (~30-40 секунд)</p>
            <input type="file" id="pdfFile" accept=".pdf" style="margin: 10px 0; padding: 10px;">
            <button onclick="uploadPDF()">🤖 AI Анализ</button>
            <button onclick="checkExpired()" style="background: #ffc107; color: #000;">⏰ Проверить сроки</button>
            <button onclick="showAuditLog()" style="background: #6c757d; color: #fff;">📈 Audit Log</button>
        </div>

        <div id="result"></div>
        <div id="documentHistory" style="margin-top: 20px;"></div>
    </div>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById('pdfFile');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<div class="result">Выберите PDF файл!</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">🤖 AI анализирует протокол через Amazon Bedrock...<br>⏱️ Примерно 30-40 секунд для 10 пользователей</div>';

            try {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                const response = await fetch('/upload-pdf', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                displayResult(data);

            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Ошибка обработки</div>';
            }
        }
        
        async function loadDocumentHistory() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('documentHistory');
                
                if (data.documents && data.documents.length > 0) {
                    let html = '<h3>📄 История обработанных документов (' + data.total_documents + '):</h3>';
                    
                    data.documents.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
                        html += `<strong>📄 ${doc.title}</strong>`;
                        html += `<button onclick="toggleDetails('doc${index}')" style="background: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">🔍 Подробности</button>`;
                        html += `</div>`;
                        html += `<div style="color: #6c757d; font-size: 12px;">⏰ ${date} | 🎯 ${doc.assignments_count} назначений</div>`;
                        
                        // Скрытые детали
                        html += `<div id="doc${index}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">`;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5>📊 Назначения курсов:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 8px; margin: 5px 0; border-radius: 3px; font-size: 12px;">`;
                                html += `📚 <strong>${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                                html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                                html += `🎯 Приоритет: ${assignment.priority} | ⏰ Назначен: ${assignDate}<br>`;
                                
                                // Добавляем дедлайн и период
                                const assignedDate = new Date(assignment.timestamp);
                                const deadlineDays = 30; // по умолчанию
                                const renewalMonths = 12; // по умолчанию
                                const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                                const renewalDate = new Date(assignedDate.getTime() + renewalMonths * 30 * 24 * 60 * 60 * 1000);
                                
                                html += `⏳ Дедлайн: ${deadlineDate.toLocaleDateString()} | 🔄 Обновление: ${renewalDate.toLocaleDateString()}`;
                                if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic;">Никому не назначались курсы</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5>⚠️ Пропущено дубликатов:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 8px; margin: 5px 0; border-radius: 3px; font-size: 12px;">`;
                                html += `😫 <strong>${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<strong>Пропущено:</strong> ${skip.skipped_courses.join(', ')}<br>`;
                                html += `<em>${skip.reason}</em>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div></div>`;
                    });
                    
                    historyDiv.innerHTML = html;
                } else {
                    historyDiv.innerHTML = '';
                }
                
            } catch (error) {
                console.error('Error loading document history:', error);
            }
        }
        
        function toggleDetails(id) {
            const element = document.getElementById(id);
            if (element.style.display === 'none') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                document.getElementById('userCount').textContent = data.users;
                document.getElementById('courseCount').textContent = data.courses;
                document.getElementById('assignmentCount').textContent = data.assignments;
                document.getElementById('documentCount').textContent = data.documents;
                document.getElementById('completionCount').textContent = data.completions || 0;
                document.getElementById('expiredCount').textContent = data.expired || 0;
                document.getElementById('criticalCount').textContent = data.critical || 0;
                document.getElementById('activeCount').textContent = data.active || 0;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function showUsers() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">👥 Загружаю список пользователей...</div>';
            
            try {
                const response = await fetch('/users-detail');
                const data = await response.json();
                
                let html = '<div class="result"><h3>👥 Пользователи (' + data.users.length + ')</h3>';
                
                data.users.forEach(user => {
                    const lastAssignment = user.latest_assignment ? new Date(user.latest_assignment).toLocaleDateString() : 'Никогда';
                    
                    html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 12px; margin: 8px 0;">`;
                    html += `<strong onclick="showUserProfile('${user.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">👤 ${user.name}</strong> (${user.user_id}) <span style="color: #007bff; font-size: 12px;">➤ Кликните для профиля</span><br>`;
                    html += `🏢 ${user.role} | ${user.department}<br>`;
                    html += `🎯 Назначений: ${user.assignments_count} | Последнее: ${lastAssignment}`;
                    html += `</div>`;
                });
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки пользователей</div>';
            }
        }
        
        async function showCourses() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">📚 Загружаю список курсов...</div>';
            
            try {
                const response = await fetch('/courses-detail');
                const data = await response.json();
                
                let html = '<div class="result"><h3>📚 Курсы (' + data.courses.length + ')</h3>';
                
                data.courses.forEach(course => {
                    const lastAssignment = course.latest_assignment ? new Date(course.latest_assignment).toLocaleDateString() : 'Никогда';
                    
                    html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 12px; margin: 8px 0;">`;
                    html += `<strong>📚 ${course.course_name}</strong> (${course.course_id})<br>`;
                    html += `📝 ${course.description}<br>`;
                    html += `🎯 Назначений: ${course.assignments_count} | Последнее: ${lastAssignment}<br>`;
                    html += `🔄 Период: ${course.renewal_months} мес. | Приоритет: ${course.priority}`;
                    html += `</div>`;
                });
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки курсов</div>';
            }
        }
        
        async function showAssignments() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">🎯 Загружаю назначения...</div>';
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                let html = '<div class="result"><h3>🎯 Последние назначения (' + data.assignments.length + ')</h3>';
                
                data.assignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 10px; margin: 8px 0; border-radius: 3px;">`;
                    html += `<strong>📚 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                    html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                    html += `🎯 Приоритет: ${assignment.priority} | ⏰ ${date}<br>`;
                    if (assignment.reason) html += `📝 ${assignment.reason}`;
                    html += `</div>`;
                });
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки назначений</div>';
            }
        }
        
        async function showDocuments() {
            loadDocumentHistory();
        }
        
        async function showExpired() {
            checkExpired();
        }
        
        async function showCritical() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">🔴 Загружаю критичные курсы...</div>';
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                const criticalAssignments = data.assignments.filter(a => a.priority === 'critical');
                
                let html = '<div class="result"><h3>🔴 Критичные курсы (' + criticalAssignments.length + ')</h3>';
                
                if (criticalAssignments.length > 0) {
                    criticalAssignments.forEach(assignment => {
                        const date = new Date(assignment.timestamp).toLocaleString();
                        
                        html += `<div style="background: #fff3cd; border-left: 4px solid #dc3545; padding: 10px; margin: 8px 0; border-radius: 3px;">`;
                        html += `<strong>🔴 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                        html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                        html += `⏰ Назначен: ${date}`;
                        if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                        html += `</div>`;
                    });
                } else {
                    html += '<p style="color: #6c757d; font-style: italic;">Нет критичных курсов</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки критичных курсов</div>';
            }
        }
        
        async function showActive() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">⚙️ Загружаю активные курсы...</div>';
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                let html = '<div class="result"><h3>⚙️ Активные курсы (в процессе)</h3>';
                html += '<p>Показываем курсы, которые назначены, но еще не завершены и не просрочены</p>';
                
                data.assignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 10px; margin: 8px 0; border-radius: 3px;">`;
                    html += `<strong>⚙️ ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                    html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                    html += `🎯 Приоритет: ${assignment.priority} | ⏰ ${date}`;
                    if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                    html += `</div>`;
                });
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки активных курсов</div>';
            }
        }
        
        async function showCompletions() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">✅ Загружаю завершенные курсы...</div>';
            
            try {
                const response = await fetch('/completions-detail');
                const data = await response.json();
                
                let html = '<div class="result"><h3>✅ Завершенные курсы (' + data.completions.length + ')</h3>';
                
                if (data.completions && data.completions.length > 0) {
                    data.completions.forEach(completion => {
                        const date = new Date(completion.completed_at).toLocaleString();
                        
                        html += `<div style="background: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 8px 0; border-radius: 3px;">`;
                        html += `<strong>✅ ${completion.course_id}</strong> → <strong onclick="showUserProfile('${completion.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${completion.user_name || completion.user_id}</strong><br>`;
                        html += `👤 ${completion.user_role || ''}, ${completion.user_department || ''}<br>`;
                        html += `⏰ Завершен: ${date} | 🎯 Метод: ${completion.completion_method}`;
                        html += `</div>`;
                    });
                } else {
                    html += '<p style="color: #6c757d; font-style: italic;">Никто еще не завершил курсы</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки завершений</div>';
            }
        }
        
        async function showUserProfile(userId) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<div class="result">👤 Загружаю профиль пользователя...</div>';
            
            try {
                const response = await fetch(`/user/${userId}`);
                const data = await response.json();
                
                if (data.error) {
                    resultDiv.innerHTML = `<div class="result">❌ ${data.error}</div>`;
                    return;
                }
                
                let html = '<div class="result">';
                html += `<h3>👤 Профиль пользователя</h3>`;
                
                // Основная информация
                html += `<div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">`;
                html += `<h4>👤 ${data.user.name} (${data.user.user_id})</h4>`;
                html += `<p><strong>🏢 Должность:</strong> ${data.user.role}</p>`;
                html += `<p><strong>🏭 Отдел:</strong> ${data.user.department}</p>`;
                html += `<p><strong>🎯 Всего назначений:</strong> ${data.total_assignments}</p>`;
                html += `<p><strong>✅ Активных курсов:</strong> ${data.active_courses}</p>`;
                
                // Добавляем детальную статистику
                const completedCount = data.assignments.filter(a => a.is_completed).length;
                const expiredCount = data.assignments.filter(a => a.is_expired && !a.is_completed).length;
                const criticalCount = data.assignments.filter(a => a.priority === 'critical' && !a.is_completed).length;
                
                html += `<div style="display: flex; gap: 10px; margin: 15px 0; flex-wrap: wrap;">`;
                html += `<div style="background: #d4edda; padding: 8px 12px; border-radius: 5px; text-align: center; flex: 1; min-width: 80px;"><strong>${data.active_courses}</strong><br><small>✅ Активных</small></div>`;
                html += `<div style="background: #cce5ff; padding: 8px 12px; border-radius: 5px; text-align: center; flex: 1; min-width: 80px;"><strong>${completedCount}</strong><br><small>✅ Завершено</small></div>`;
                html += `<div style="background: #f8d7da; padding: 8px 12px; border-radius: 5px; text-align: center; flex: 1; min-width: 80px;"><strong>${expiredCount}</strong><br><small>❌ Просрочено</small></div>`;
                html += `<div style="background: #fff3cd; padding: 8px 12px; border-radius: 5px; text-align: center; flex: 1; min-width: 80px;"><strong>${criticalCount}</strong><br><small>🔴 Критичных</small></div>`;
                html += `</div>`;
                
                html += `<p><a href="/user/${userId}/dashboard" target="_blank" style="background: #007bff; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px;">📊 Открыть личный кабинет</a></p>`;
                html += `</div>`;
                
                // Назначенные курсы
                if (data.assignments && data.assignments.length > 0) {
                    html += `<h4>📚 Назначенные курсы (${data.assignments.length})</h4>`;
                    
                    data.assignments.forEach(assignment => {
                        const date = new Date(assignment.timestamp).toLocaleString();
                        const priorityColors = {
                            'critical': '#dc3545',
                            'high': '#fd7e14', 
                            'normal': '#28a745',
                            'low': '#6c757d'
                        };
                        
                        const statusColor = assignment.is_expired ? '#dc3545' : '#28a745';
                        const statusText = assignment.is_expired ? '❌ Истек' : '✅ Активен';
                        
                        html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 5px;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center;">`;
                        html += `<strong>📚 ${assignment.course_id}</strong>`;
                        html += `<span style="color: ${statusColor}; font-weight: bold;">${statusText}</span>`;
                        html += `</div>`;
                        html += `<div style="margin: 8px 0; font-size: 13px;">`;
                        html += `🎯 Приоритет: ${assignment.priority}<br>`;
                        html += `🔄 Период: ${assignment.renewal_months} мес. | ⏰ Дедлайн: ${assignment.deadline_days} дней<br>`;
                        html += `⏰ Назначен: ${date}`;
                        if (assignment.reason) html += `<br>📝 Причина: ${assignment.reason}`;
                        html += `</div></div>`;
                    });
                } else {
                    html += '<p style="color: #6c757d; font-style: italic;">Нет назначенных курсов</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки профиля</div>';
            }
        }
        
        // Загружаем статистику и историю при загрузке страницы
        window.onload = function() {
            loadStats();
            loadDocumentHistory();
        }

        function displayResult(data) {
            const resultDiv = document.getElementById('result');
            
            let html = '<div class="result">';
            
            // Проверяем, является ли документ дубликатом
            if (data.is_duplicate) {
                html += '<h3>⚠️ Документ уже обрабатывался!</h3>';
                html += `<p><strong>Предыдущая обработка:</strong> ${data.previous_processing.processed_at}</p>`;
                html += `<p><strong>Назначений тогда:</strong> ${data.previous_processing.assignments_count}</p>`;
                html += `<p><strong>Пользователи:</strong> ${data.previous_processing.assigned_users.join(', ')}</p>`;
                
                if (data.extracted_text) {
                    html += `<p><strong>Протокол:</strong> ${data.extracted_text}</p>`;
                }
            } else {
                html += `<h3>✅ AI анализ завершен для ${data.total_users} пользователей</h3>`;
                
                if (data.extracted_text) {
                    html += `<p><strong>Протокол:</strong> ${data.extracted_text}</p>`;
                }
                
                if (data.assignments && data.assignments.length > 0) {
                    html += `<h4>🎯 AI назначил курсы (${data.assignments.length} пользователей):</h4>`;
                    
                    data.assignments.forEach(assignment => {
                        html += `<div class="assignment">`;
                        html += `<strong>${assignment.name}</strong> (${assignment.user_id}) - ${assignment.role}, ${assignment.department}<br>`;
                        html += `<strong>Курсы с AI-определенными сроками:</strong><br> `;
                        assignment.courses_assigned.forEach(courseId => {
                            html += `<span class="course">📚 ${courseId}</span> `;
                        });
                        if (assignment.reason) {
                            html += `<br><em>AI обоснование: ${assignment.reason}</em>`;
                        }
                        if (assignment.course_periods) {
                            html += `<br><strong>🔄 AI определил:</strong><br> `;
                            assignment.course_periods.forEach(period => {
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#17a2b8',
                                    'low': '#6c757d'
                                };
                                const priorityNames = {
                                    'critical': '🔴 Критичный',
                                    'high': '🟠 Высокий',
                                    'normal': '🟢 Обычный',
                                    'low': '⚪ Низкий'
                                };
                                
                                html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[period.priority] || '#17a2b8'}; padding: 10px; margin: 6px 0; border-radius: 5px; font-size: 13px;">`;
                                html += `📚 <strong>${period.course_id}</strong><br>`;
                                html += `🎯 Приоритет: ${priorityNames[period.priority] || period.priority}<br>`;
                                html += `🔄 Периодичность: каждые ${period.months} мес.<br>`;
                                html += `⏰ Дедлайн: ${period.deadline_days} дней`;
                                html += `</div>`;
                            });
                        }
                        html += `</div>`;
                    });
                } else {
                    html += '<p>AI определил: никому не нужны новые курсы по этому протоколу</p>';
                }
                
                // Показываем пропущенные дубликаты
                if (data.skipped_duplicates && data.skipped_duplicates.length > 0) {
                    html += `<h4>⚠️ Пропущено дубликатов (${data.skipped_duplicates.length} пользователей):</h4>`;
                    
                    data.skipped_duplicates.forEach(skip => {
                        html += `<div style="background: #fff3cd; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #ffc107;">`;
                        html += `<strong>${skip.name}</strong> (${skip.user_id})<br>`;
                        html += `<strong>Пропущено:</strong> `;
                        skip.skipped_courses.forEach(courseId => {
                            html += `<span style="background: #f8d7da; padding: 4px 8px; margin: 2px; border-radius: 3px; display: inline-block;">🚫 ${courseId}</span> `;
                        });
                        html += `<br><em>${skip.reason}</em>`;
                        html += `</div>`;
                    });
                }
            }
            
            html += '</div>';
            resultDiv.innerHTML = html;
            
            // Обновляем статистику и историю
            loadStats();
            loadDocumentHistory();
        }
        
        async function checkExpired() {
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = '<div class="result">⏰ Проверяю сроки курсов...</div>';
            
            try {
                const response = await fetch('/expired-courses');
                const data = await response.json();
                
                let html = '<div class="result">';
                html += `<h3>⏰ Проверка сроков курсов</h3>`;
                
                if (data.expired_users && data.expired_users.length > 0) {
                    html += `<h4>⚠️ Найдено ${data.expired_count} пользователей с истекающими курсами:</h4>`;
                    
                    data.expired_users.forEach(user => {
                        html += `<div style="background: #fff3cd; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #ffc107;">`;
                        html += `<strong>${user.user_name || user.user_id}</strong> - ${user.role || ''}, ${user.department || ''}<br>`;
                        html += `<strong>Истекающие курсы:</strong><br>`;
                        
                        user.expired_courses.forEach(course => {
                            html += `<div style="margin: 5px 0; padding: 5px; background: #f8d7da; border-radius: 3px;">`;
                            html += `🚨 <strong>${course.course_id}</strong><br>`;
                            html += `Назначен: ${new Date(course.assigned_at).toLocaleDateString()}<br>`;
                            html += `Период: ${course.period_months} месяцев`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    });
                } else {
                    html += '<p>✅ Все курсы актуальны!</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Ошибка проверки сроков</div>';
            }
        }
        
        async function showAuditLog() {
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = '<div class="result">📈 Загружаю audit log...</div>';
            
            try {
                const response = await fetch('/audit-log');
                const data = await response.json();
                
                let html = '<div class="result">';
                html += `<h3>📈 Audit Log - Последние ${data.total_logs} действий</h3>`;
                
                if (data.logs && data.logs.length > 0) {
                    data.logs.forEach(log => {
                        const date = new Date(log.timestamp).toLocaleString();
                        
                        if (log.action === 'course_assigned') {
                            const priorityColors = {
                                'critical': '#dc3545',
                                'high': '#fd7e14', 
                                'normal': '#28a745',
                                'low': '#6c757d'
                            };
                            
                            html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[log.priority] || '#28a745'}; padding: 10px; margin: 8px 0; border-radius: 5px; font-size: 13px;">`;
                            html += `<strong>📚 Курс назначен:</strong> ${log.course_id}<br>`;
                            html += `👤 <strong>Пользователь:</strong> ${log.user_name || log.user_id} (${log.user_role || ''}, ${log.user_department || ''})<br>`;
                            html += `🤖 <strong>Назначил:</strong> ${log.assigned_by}<br>`;
                            html += `🎯 <strong>Приоритет:</strong> ${log.priority}<br>`;
                            if (log.reason) html += `📝 <strong>Причина:</strong> ${log.reason}<br>`;
                            html += `⏰ <strong>Время:</strong> ${date}`;
                            html += `</div>`;
                        } else if (log.action === 'document_processed') {
                            html += `<div style="background: #e7f3ff; border-left: 4px solid #007bff; padding: 10px; margin: 8px 0; border-radius: 5px; font-size: 13px;">`;
                            html += `<strong>📄 Документ обработан</strong><br>`;
                            html += `📝 <strong>Протокол:</strong> ${log.protocol_title}<br>`;
                            html += `🎯 <strong>Назначений:</strong> ${log.assignments_count}<br>`;
                            html += `⏰ <strong>Время:</strong> ${date}`;
                            html += `</div>`;
                        }
                    });
                } else {
                    html += '<p>ℹ️ Лог пуст</p>';
                }
                
                html += '</div>';
                resultDiv.innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки audit log</div>';
            }
        }
    </script>
</body>
</html>
    '''
    return HTMLResponse(content=html)

@app.get("/users-detail")
async def get_users_detail():
    """Получить детальную информацию о пользователях"""
    users = mentor.db.get_all_users()
    
    # Добавляем информацию о назначенных курсах
    for user in users:
        user_assignments = [log for log in audit_logger.logs if log.get("user_id") == user["user_id"] and log.get("action") == "course_assigned"]
        user["assignments_count"] = len(user_assignments)
        user["latest_assignment"] = user_assignments[0]["timestamp"] if user_assignments else None
    
    return {"users": users}

@app.get("/courses-detail")
async def get_courses_detail():
    """Получить детальную информацию о курсах"""
    courses = mentor.db.get_all_courses()
    
    # Добавляем статистику назначений
    for course in courses:
        course_assignments = [log for log in audit_logger.logs if log.get("course_id") == course["course_id"] and log.get("action") == "course_assigned"]
        course["assignments_count"] = len(course_assignments)
        course["latest_assignment"] = course_assignments[0]["timestamp"] if course_assignments else None
        
        # Добавляем AI-определенную периодичность
        course["renewal_months"] = scheduler.course_periods.get(course["course_id"], "N/A")
        course["priority"] = getattr(scheduler, 'course_priorities', {}).get(course["course_id"], "N/A")
    
    return {"courses": courses}

@app.post("/complete-course")
async def complete_course(user_id: str = Form(...), course_id: str = Form(...)):
    """Отмечает курс как пройденный"""
    try:
        # Проверяем, что пользователь существует
        user = mentor.db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Проверяем, не пройден ли уже курс
        if course_completion.is_course_completed(user_id, course_id):
            return {"message": "Курс уже отмечен как пройденный", "success": False}
        
        # Отмечаем курс как пройденный
        completion = course_completion.complete_course(user_id, course_id, "manual")
        
        # Логируем завершение
        audit_logger.logs.append({
            "timestamp": completion["completed_at"],
            "action": "course_completed",
            "user_id": user_id,
            "course_id": course_id,
            "completion_method": "manual",
            "id": len(audit_logger.logs) + 1
        })
        audit_logger.save_logs()
        
        return {
            "message": f"Курс {course_id} успешно отмечен как пройденный!",
            "success": True,
            "completion": completion
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/dashboard")
async def get_user_dashboard(user_id: str):
    """Получить пользовательскую страницу (как видит пользователь)"""
    user = mentor.db.get_user(user_id)
    if not user:
        return HTMLResponse(content="<h1>Пользователь не найден</h1>")
    
    # Получаем все назначения пользователя
    assignments = [log for log in audit_logger.logs if log.get("user_id") == user_id and log.get("action") == "course_assigned"]
    
    # Добавляем информацию о курсах
    for assignment in assignments:
        course_id = assignment.get("course_id")
        if course_id:
            assignment["is_expired"] = scheduler.is_course_expired(course_id, assignment["timestamp"])
            assignment["renewal_months"] = scheduler.course_periods.get(course_id, "N/A")
            assignment["deadline_days"] = getattr(scheduler, 'course_deadlines', {}).get(course_id, 30)
            assignment["is_completed"] = course_completion.is_course_completed(user_id, course_id)
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    user_data = {"user": user}
    html = generate_user_dashboard_html(user_data, assignments, scheduler, course_completion)
    
    return HTMLResponse(content=html)

@app.get("/user/{user_id}")
async def get_user_profile(user_id: str):
    """Получить полный профиль пользователя"""
    user = mentor.db.get_user(user_id)
    if not user:
        return {"error": "Пользователь не найден"}
    
    # Получаем все назначения пользователя
    assignments = [log for log in audit_logger.logs if log.get("user_id") == user_id and log.get("action") == "course_assigned"]
    
    # Добавляем информацию о курсах
    for assignment in assignments:
        course_id = assignment.get("course_id")
        if course_id:
            # Проверяем срок действия
            assignment["is_expired"] = scheduler.is_course_expired(course_id, assignment["timestamp"])
            assignment["renewal_months"] = scheduler.course_periods.get(course_id, "N/A")
            assignment["deadline_days"] = getattr(scheduler, 'course_deadlines', {}).get(course_id, "N/A")
            assignment["is_completed"] = course_completion.is_course_completed(user_id, course_id)
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Получаем историю из трекера документов
    tracker_history = doc_tracker.get_user_history(user_id)
    
    return {
        "user": user,
        "assignments": assignments,
        "tracker_history": tracker_history,
        "total_assignments": len(assignments),
        "active_courses": len([a for a in assignments if not a.get("is_expired", False) and not a.get("is_completed", False)])
    }

@app.get("/assignments-detail")
async def get_assignments_detail():
    """Получить детальную информацию о назначениях"""
    assignments = [log for log in audit_logger.logs if log.get("action") == "course_assigned"]
    
    # Добавляем информацию о пользователях
    for assignment in assignments:
        if assignment.get("user_id"):
            user = mentor.db.get_user(assignment["user_id"])
            if user:
                assignment["user_name"] = user["name"]
                assignment["user_role"] = user["role"]
                assignment["user_department"] = user["department"]
    
    # Сортируем по дате
    assignments.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {"assignments": assignments[:50]}  # Последние 50

@app.get("/stats")
async def get_stats():
    """Получить статистику системы"""
    # Количество пользователей
    users = mentor.db.get_all_users()
    user_count = len(users)
    
    # Количество курсов
    courses = mentor.db.get_all_courses()
    course_count = len(courses)
    
    # Количество назначений (из audit log)
    assignment_logs = [log for log in audit_logger.logs if log.get("action") == "course_assigned"]
    assignment_count = len(assignment_logs)
    
    # Количество обработанных документов
    document_count = len(doc_tracker.processed_docs)
    
    # Количество завершенных курсов
    completion_stats = course_completion.get_completion_stats()
    
    # Подсчитываем дополнительную статистику
    expired_count = 0
    critical_count = 0
    active_count = 0
    
    for log in assignment_logs:
        user_id = log.get("user_id")
        course_id = log.get("course_id")
        if user_id and course_id:
            is_expired = scheduler.is_course_expired(course_id, log["timestamp"])
            is_completed = course_completion.is_course_completed(user_id, course_id)
            priority = log.get("priority", "normal")
            
            if is_expired and not is_completed:
                expired_count += 1
            elif not is_expired and not is_completed:
                active_count += 1
                if priority == "critical":
                    critical_count += 1
    
    return {
        "users": user_count,
        "courses": course_count,
        "assignments": assignment_count,
        "documents": document_count,
        "completions": completion_stats["total_completions"],
        "expired": expired_count,
        "critical": critical_count,
        "active": active_count
    }

@app.get("/document-history")
async def get_document_history():
    """Получить историю обработанных документов"""
    documents = []
    
    # Проходим по всем обработанным документам
    for doc_hash, doc_info in doc_tracker.processed_docs.items():
        # Находим все назначения, сделанные в то же время
        doc_minute = doc_info["processed_at"][:16]  # 2025-09-18T13:29
        
        doc_assignments = []
        for log in audit_logger.logs:
            if log.get("action") == "course_assigned":
                # Новые документы - по хэшу, старые - по времени
                if (log.get("document_hash") == doc_hash or 
                    (not log.get("document_hash") and log.get("timestamp", "")[:16] == doc_minute)):
                    
                    user = mentor.db.get_user(log["user_id"])
                    if user:
                        log["user_name"] = user["name"]
                        log["user_role"] = user["role"]
                        log["user_department"] = user["department"]
                    
                    doc_assignments.append(log)
        
        # Получаем сохраненные skipped_duplicates
        skipped_info = doc_info.get("skipped_duplicates", [])
        
        documents.append({
            "hash": doc_hash,
            "title": doc_info["title"],
            "processed_at": doc_info["processed_at"],
            "assignments_count": len(doc_assignments),
            "assignments": doc_assignments,
            "skipped_duplicates": skipped_info  # Добавляем пропущенные
        })
    
    # Сортируем по дате
    documents.sort(key=lambda x: x["processed_at"], reverse=True)
    
    return {
        "total_documents": len(documents),
        "documents": documents
    }

@app.get("/audit-log")
async def get_audit_log():
    """Получить audit log"""
    recent_logs = audit_logger.get_recent_logs(100)
    
    # Добавляем информацию о пользователях
    for log in recent_logs:
        if log.get("user_id"):
            user = mentor.db.get_user(log["user_id"])
            if user:
                log["user_name"] = user["name"]
                log["user_role"] = user["role"]
                log["user_department"] = user["department"]
    
    return {
        "total_logs": len(recent_logs),
        "logs": recent_logs
    }

@app.get("/completions-detail")
async def get_completions_detail():
    """Получить детальную информацию о завершенных курсах"""
    completions = course_completion.completions.copy()
    
    # Добавляем информацию о пользователях
    for completion in completions:
        if completion.get("user_id"):
            user = mentor.db.get_user(completion["user_id"])
            if user:
                completion["user_name"] = user["name"]
                completion["user_role"] = user["role"]
                completion["user_department"] = user["department"]
    
    # Сортируем по дате
    completions.sort(key=lambda x: x["completed_at"], reverse=True)
    
    return {"completions": completions[:50]}  # Последние 50

@app.get("/expired-courses")
async def get_expired_courses():
    """Получить список пользователей с истекающими курсами"""
    expired_list = scheduler.get_expired_courses(doc_tracker)
    
    # Получаем информацию о пользователях
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)