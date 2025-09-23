from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from ai_mentor import AIMentor
from pdf_processor import extract_text_from_pdf
from document_tracker import DocumentTracker
from course_scheduler import CourseScheduler
from audit_logger import AuditLogger
from user_dashboard import generate_user_dashboard_html
from course_completion import CourseCompletion

app = FastAPI(title="EHS AI Mentor", version="1.0.0")

# Добавляем обработку статических файлов
@app.get("/calpoly-logo.png")
async def get_logo():
    return FileResponse("calpoly-logo.png")

@app.get("/tahoe.css")
async def get_tahoe_css():
    return FileResponse("tahoe.css", media_type="text/css")

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
        
        # Логируем обработку document
        audit_logger.log_document_processed(
            doc_hash, 
            len(result.get("assignments", [])),
            protocol_text[:100] + "..."
        )
        
        # Логируем каждое назначение с хэшем document
        for assignment in result.get("assignments", []):
            for course_id in assignment["courses_assigned"]:
                clean_course_id = course_id.replace(" (обновление)", "")
                priority = "normal"
                if assignment.get("course_periods"):
                    for period in assignment["course_periods"]:
                        if period["course_id"] == clean_course_id:
                            priority = period.get("priority", "normal")
                            break
                
                # Добавляем хэш document в лог
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
        
        # Добавляем информацию об истекающих courseх
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
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
      background: #f5f5f5;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    
    .appbar {
      background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%);
      border-radius: 12px;
      padding: 20px;
      color: white;
      margin-bottom: 20px;
    }
    
    .hero {
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    button {
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      background: #007AFF;
      color: white;
      cursor: pointer;
    }
    
    button:hover {
      background: #0056CC;
    }
    
    .stat-card {
      background: white;
      padding: 15px;
      border-radius: 8px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .stat-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    
    .training-card {
      background: white;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 15px;
      display: flex;
      align-items: center;
      gap: 15px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .training-content {
      flex: 1;
    }
    
    .training-btn {
      background: #007AFF;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
    }
    
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal.show {
      display: flex;
    }
    
    .modal-content {
      background: white;
      border-radius: 12px;
      max-width: 800px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .modal-header {
      padding: 20px;
      border-bottom: 1px solid #eee;
      position: relative;
    }
    
    .modal-body {
      padding: 20px;
    }
    
    .modal-close {
      position: absolute;
      top: 10px;
      right: 15px;
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: #999;
    }
    
    .modal-close:hover {
      color: #333;
    }
    </style>
</head>
<body>
    <header class="appbar">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 28px; font-weight: 700;">👋 Hello, Admin</div>
                <div style="font-size: 20px; opacity: 0.9;">✨ Managing EHS training for everyone</div>
            </div>
            <button onclick="logout()">Logout</button>
        </div>
    </header>
    
    <div class="container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="hero">
                <h1>📊 System Statistics</h1>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 16px; margin-top: 20px;">
                    <div class="stat-card" onclick="showUsers()">
                        <div style="font-size: 24px; font-weight: 700; color: #007AFF;" id="userCount">-</div>
                        <div style="font-size: 12px; color: #666;">👥 Users</div>
                    </div>
                    <div class="stat-card" onclick="showCourses()">
                        <div style="font-size: 24px; font-weight: 700; color: #AF52DE;" id="courseCount">-</div>
                        <div style="font-size: 12px; color: #666;">📚 Courses</div>
                    </div>
                    <div class="stat-card" onclick="showAssignments()">
                        <div style="font-size: 24px; font-weight: 700; color: #34C759;" id="assignmentCount">-</div>
                        <div style="font-size: 12px; color: #666;">🎯 Assignments</div>
                    </div>
                    <div class="stat-card" onclick="showDocuments()">
                        <div style="font-size: 24px; font-weight: 700; color: #FF9500;" id="documentCount">-</div>
                        <div style="font-size: 12px; color: #666;">📄 Documents</div>
                    </div>
                </div>
            </div>
            
            <div class="hero" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%); color: white;">
                <h1>🤖 AI Processing</h1>
                <p>⚡ Processing first 10 users for demonstration (~30-40 seconds)</p>
                <input type="file" id="pdfFile" accept=".pdf" style="width: 100%; margin: 16px 0; padding: 16px; border: 2px dashed rgba(255,255,255,0.3); border-radius: 16px; background: rgba(255,255,255,0.1); color: white;">
                <div style="display: flex; gap: 12px; margin-top: 24px;">
                    <button onclick="uploadPDF()" style="background: #ff8533; flex: 1;">🤖 AI Analysis</button>
                    <button onclick="showAuditLog()" style="background: rgba(255,255,255,0.2); flex: 1;">📈 Audit Log</button>
                </div>
            </div>
        </div>
        
        <div class="hero" id="documentHistory"></div>
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
        function logout() {
            if(confirm('Are you sure you want to logout?')) {
                window.location.href = './index.html';
            }
        }
        
        function showModal(title, content) {
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalBody').innerHTML = content;
            document.getElementById('mainModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('mainModal').classList.remove('show');
        }
        
        async function uploadPDF() {
            const fileInput = document.getElementById('pdfFile');
            
            if (!fileInput.files[0]) {
                showModal('⚠️ Error', '<div style="text-align: center; padding: 40px; color: #dc3545;">Please select a PDF file!</div>');
                return;
            }

            showModal('🤖 AI Analysis', '<div style="text-align: center; padding: 40px;">🤖 AI analyzing protocol via Amazon Bedrock...<br><br>⏱️ Approximately 30-40 seconds for 10 users</div>');

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
                showModal('❌ Error', '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Processing error</div>');
            }
        }
        
        function displayResult(data) {
            let html = '';
            let title = '';
            
            if (data.is_duplicate) {
                title = '⚠️ Документ уже обрабатывался';
                html += '<h4>⚠️ Документ уже обрабатывался!</h4>';
                html += `<div style="background: #fff3cd; padding: 16px; border-radius: 8px; margin: 16px 0;">`;
                html += `<div style="margin: 8px 0;"><strong>Предыдущая обработка:</strong> ${data.previous_processing.processed_at}</div>`;
                html += `<div style="margin: 8px 0;"><strong>Назначений тогда:</strong> ${data.previous_processing.assignments_count}</div>`;
                html += `</div>`;
            } else {
                title = `✅ AI анализ завершен`;
                html += `<h4>✅ AI анализ завершен для ${data.total_users} пользователей</h4>`;
                
                if (data.assignments && data.assignments.length > 0) {
                    html += `<h5>🎯 AI назначил курсы (${data.assignments.length} пользователей):</h5>`;
                    
                    data.assignments.forEach(assignment => {
                        html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                        html += `<strong style="font-size: 18px; color: #2a7d2e;">${assignment.name}</strong> (${assignment.user_id}) - ${assignment.role}, ${assignment.department}<br>`;
                        html += `<div style="margin: 12px 0;"><strong>Курсы:</strong></div>`;
                        assignment.courses_assigned.forEach(courseId => {
                            html += `<span style="background: #e8f5e8; padding: 6px 12px; margin: 4px; border-radius: 6px; display: inline-block;">📚 ${courseId}</span> `;
                        });
                        if (assignment.reason) {
                            html += `<div style="margin: 12px 0; font-style: italic; color: #666;">AI обоснование: ${assignment.reason}</div>`;
                        }
                        html += `</div>`;
                    });
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #666;">AI определил: никому не нужны новые курсы по этому протоколу</div>';
                }
            }
            
            showModal(title, html);
            loadStats();
            loadDocumentHistory();
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                document.getElementById('userCount').textContent = data.users;
                document.getElementById('courseCount').textContent = data.courses;
                document.getElementById('assignmentCount').textContent = data.assignments;
                document.getElementById('documentCount').textContent = data.documents;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadDocumentHistory() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('documentHistory');
                
                if (data.documents && data.documents.length > 0) {
                    let html = '<h1>📄 Processed Documents (' + data.total_documents + ')</h1><div>';
                    
                    data.documents.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div class="training-card">`;
                        html += `<div class="training-content">`;
                        html += `<h3>📄 ${doc.title}</h3>`;
                        html += `<p>Обработан ${date}</p>`;
                        html += `<p>🎯 ${doc.assignments_count} назначений</p>`;
                        html += `</div>`;
                        html += `<button class="training-btn" onclick="showDocumentDetails(${index})">Details</button>`;
                        html += `</div>`;
                    });
                    
                    html += '</div>';
                    historyDiv.innerHTML = html;
                } else {
                    historyDiv.innerHTML = '<h1>📄 Processed Documents</h1><div style="text-align: center; padding: 40px;"><h3>No processed documents</h3><p>Upload your first PDF protocol for analysis!</p></div>';
                }
                
            } catch (error) {
                console.error('Error loading document history:', error);
            }
        }
        
        async function showDocumentDetails(index) {
            showModal('📄 Document Details', '<div style="text-align: center; padding: 40px;">📄 Loading document details...</div>');
            
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                const doc = data.documents[index];
                
                if (doc) {
                    let html = `<h4>📄 ${doc.title}</h4>`;
                    html += `<p>⏰ Processed: ${new Date(doc.processed_at).toLocaleString()}</p>`;
                    
                    if (doc.assignments && doc.assignments.length > 0) {
                        html += `<h5>📊 Course Assignments:</h5>`;
                        doc.assignments.forEach(assignment => {
                            html += `<div style="background: #f8f9fa; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                            html += `<strong>📚 ${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                            html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                            html += `🎯 Priority: ${assignment.priority} | ⏰ ${new Date(assignment.timestamp).toLocaleString()}`;
                            if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                            html += `</div>`;
                        });
                    } else {
                        html += '<p>No course assignments</p>';
                    }
                    
                    document.getElementById('modalBody').innerHTML = html;
                } else {
                    document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Document not found</div>';
                }
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading document details</div>';
            }
        }
        
        async function showUsers() {
            showModal('👥 Users', '<div style="text-align: center; padding: 40px;">👥 Loading users...</div>');
            // Add users loading logic here
        }
        
        async function showCourses() {
            showModal('📚 Courses', '<div style="text-align: center; padding: 40px;">📚 Loading courses...</div>');
            // Add courses loading logic here
        }
        
        async function showAssignments() {
            showModal('🎯 Assignments', '<div style="text-align: center; padding: 40px;">🎯 Loading assignments...</div>');
            // Add assignments loading logic here
        }
        
        async function showDocuments() {
            showModal('📄 Documents', '<div style="text-align: center; padding: 40px;">📄 Loading documents...</div>');
            // Add documents loading logic here
        }
        
        async function showAuditLog() {
            showModal('📈 Audit Log', '<div style="text-align: center; padding: 40px;">📈 Loading audit log...</div>');
            // Add audit log loading logic here
        }
        
        window.onload = function() {
            loadStats();
            loadDocumentHistory();
        }
    </script>
</body>
</html>
    '''
    return HTMLResponse(content=html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)