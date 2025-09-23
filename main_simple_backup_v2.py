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
    <link rel="stylesheet" href="/tahoe.css">
    <style>
    :root {
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
      
      /* Aliases for compatibility */
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
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      font-size: var(--text-s);
      line-height: 1.6;
      color: var(--gray-800);
      background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 50%, #86efac 100%);
      min-height: 100vh;
    }

    .container {
      max-width: var(--container-max);
      margin: 0 auto;
      padding: 0 var(--container-pad);
    }
    
    .appbar{
      background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%);
      color:#fff; padding:18px 0; position:sticky; top:0; z-index:20; box-shadow:var(--shadow-1);
      border-radius: 8px;
      margin-bottom: var(--space-m);
    }
    
    .hero{
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: var(--space-xl);
      margin: var(--space-l) 0;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .hero h1{
      font-size: var(--text-xl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }
    
    h1 {
      font-size: var(--text-xxl);
      font-weight: 700;
      line-height: 1.1;
      margin: 0 0 var(--space-l) 0;
      color: var(--gray-900);
    }

    h2 {
      font-size: var(--text-xl);
      font-weight: 600;
      line-height: 1.2;
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-900);
    }

    h3 {
      font-size: var(--text-l);
      font-weight: 600;
      line-height: 1.3;
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-800);
    }

    p {
      margin: 0 0 var(--space-m) 0;
      color: var(--gray-600);
    }
    
    button {
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
    }
    
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(14, 122, 78, 0.4);
    }
    
    button:active {
      transform: translateY(0) scale(0.98);
    }
    
    .btn {
      border: none;
      border-radius: 8px;
      padding: var(--space-xs) var(--space-s);
      font-weight: 500;
      font-size: var(--text-xs);
      cursor: pointer;
      transition: all var(--speed);
      background: var(--brand);
      color: white;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    
    .btn:hover {
      filter: brightness(.95);
      transform: translateY(-1px);
    }
    
    .tahoe-stat-card {
      background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
      padding: var(--space-s);
      border-radius: 12px;
      text-align: center;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
      transition: all var(--speed);
      border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    .tahoe-stat-card:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .training-card {
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
    }
    
    .training-card::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: var(--brand);
      border-radius: 4px 0 0 4px;
    }
    
    .training-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .training-content {
      flex: 1;
    }
    
    .training-title {
      margin: 0 0 var(--space-s) 0;
      display: flex;
      align-items: center;
      gap: var(--space-s);
      font-weight: 600;
      font-size: var(--text-l);
      color: var(--gray-800);
    }
    
    .training-desc {
      margin: 0 0 var(--space-s) 0;
      color: var(--gray-600);
      font-size: var(--text-xs);
    }
    
    .training-meta {
      display: flex;
      gap: var(--space-s);
      font-size: var(--text-xs);
      color: var(--gray-500);
    }
    
    .training-btn {
      background: var(--brand);
      color: white;
      border: none;
      padding: var(--space-xs) var(--space-s);
      border-radius: 8px;
      cursor: pointer;
      font-weight: 500;
      font-size: var(--text-xs);
      transition: all var(--speed);
    }
    
    .training-btn:hover {
      filter: brightness(.95);
      transform: translateY(-1px);
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
      background: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(20px);
      border-radius: 16px;
      max-width: 800px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .modal-header {
      padding: var(--space-l);
      border-bottom: 1px solid var(--gray-200);
      position: relative;
    }
    
    .modal-body {
      padding: var(--space-l);
    }
    
    .modal-close {
      position: absolute;
      top: 10px;
      right: 15px;
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--gray-500);
      transition: color var(--speed);
    }
    
    .modal-close:hover {
      color: var(--gray-800);
    }
    </style>
</head>
<body>

    
    <div class="container">
        
        <!-- Header в виде карточки -->
        <div class="hero" style="background: linear-gradient(135deg, #2a7d2e 0%, #66d36f 100%); color: white; grid-column: 1 / -1; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 16px;">
                <div style="display: flex; align-items: center; gap: 24px;">
                    <img src="/calpoly-logo.png" alt="Cal Poly" height="64" style="filter: brightness(0) invert(1);">
                    <div>
                        <div style="font-size: 28px; font-weight: 700; color: white; letter-spacing: -0.01em;">👋 Hello, <strong>Admin</strong></div>
                        <div style="font-size: 20px; color: rgba(255, 255, 255, 0.9); margin-top: 4px; font-weight: 500;">✨ Managing EHS training for everyone</div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 16px;">
                    <button onclick="logout()" style="background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3);">Logout</button>
                </div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="hero" style="background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px);">
                <h1 style="font-size: 48px; font-weight: 800;">📊 System Statistics</h1>
                
                <!-- Прогресс бар -->
                <div style="margin: var(--space-l) 0;">
                    <div style="background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%); backdrop-filter: blur(10px); border-radius: 16px; padding: var(--space-l); border: 1px solid rgba(255, 255, 255, 0.3);">
                        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: var(--space-s);">
                            <span style="font-weight: 600; color: var(--gray-800); font-size: var(--text-l);">Training Progress</span>
                            <span style="font-weight: 700; color: var(--brand); font-size: var(--text-l);" id="progressPercent">0%</span>
                        </div>
                        <div style="position: relative; height: 12px; border-radius: 999px; background: rgba(200,200,200,0.4); overflow: hidden; margin: var(--space-s) 0;">
                            <div id="progressFill" style="height: 100%; width: 0%; background: linear-gradient(90deg, var(--brand), var(--success)); transition: width 0.6s ease; border-radius: 999px;"></div>
                        </div>
                        <div style="display: flex; gap: var(--space-m); margin-top: var(--space-s); font-size: var(--text-xs); color: var(--gray-700);">
                            <span><strong id="completedCount" style="color: var(--success);">0</strong> Completed</span>
                            <span><strong id="totalAssignments" style="color: var(--gray-800);">0</strong> Total</span>
                            <span><strong id="activeUsers" style="color: var(--blue);">0</strong> Active Users</span>
                        </div>
                    </div>
                </div>
                
                <div id="statsBlocks" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 16px;">
            <div class="tahoe-stat-card" onclick="showUsers()" style="background: linear-gradient(145deg, #dbeafe 0%, #bfdbfe 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--blue);" id="userCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">👥 Users</div>
            </div>
            <div class="tahoe-stat-card" onclick="showCourses()" style="background: linear-gradient(145deg, #ede9fe 0%, #ddd6fe 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--purple);" id="courseCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">📚 Courses</div>
            </div>
            <div class="tahoe-stat-card" onclick="showAssignments()" style="background: linear-gradient(145deg, #dcfce7 0%, #bbf7d0 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--brand);" id="assignmentCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">🎯 Assignments</div>
            </div>
            <div class="tahoe-stat-card" onclick="showDocuments()" style="background: linear-gradient(145deg, #fed7aa 0%, #fdba74 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--orange);" id="documentCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">📄 Documents</div>
            </div>
            <div class="tahoe-stat-card" onclick="showCompletions()" style="background: linear-gradient(145deg, #dcfce7 0%, #bbf7d0 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--success);" id="completionCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">✅ Completed</div>
            </div>
            <div class="tahoe-stat-card" onclick="showExpired()" style="background: linear-gradient(145deg, #fecaca 0%, #fca5a5 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--red);" id="expiredCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">❌ Expired</div>
            </div>
            <div class="tahoe-stat-card" onclick="showCritical()" style="background: linear-gradient(145deg, #fed7aa 0%, #fdba74 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--orange);" id="criticalCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">🔴 Critical</div>
            </div>
            <div class="tahoe-stat-card" onclick="showActive()" style="background: linear-gradient(145deg, #dbeafe 0%, #bfdbfe 100%); border: none;">
                <div style="font-size: 24px; font-weight: 700; color: var(--blue);" id="activeCount">-</div>
                <div style="font-size: 12px; color: var(--gray-600); font-weight: 500; white-space: nowrap;">⚙️ Active</div>
            </div>
                </div>
            </div>
            
            <!-- Правая колонка - форма обработки -->
            <div class="hero" style="background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 50%, #f97316 100%) !important; color: white !important; border-radius: 32px !important; box-shadow: 0 20px 40px rgba(245, 158, 11, 0.3) !important;">
                <h1 style="font-size: 46px; font-weight: 800;">🤖 AI Processing</h1>
                <p style="opacity:.85;margin:0 0 16px;font-size:15px;line-height:1.5;">⚡ Processing first 10 users for demonstration (~30-40 seconds)</p>
                
                <div style="margin:24px 0;">
                    <h3 style="margin:0 0 12px;font-weight:800;font-size:20px;">Upload PDF File</h3>
                    <div style="display:flex;gap:12px;margin:0 0 24px;align-items:center;">
                        <span style="font-size:13px;opacity:.7;">PDF protocol</span>
                        <span style="font-size:13px;opacity:.7;">AI analysis</span>
                    </div>
                </div>
                <div style="position: relative; width: 100%; margin: 24px 0;">
                    <input type="file" id="pdfFile" accept=".pdf" style="position: absolute; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 2;">
                    <div style="min-height: 120px; padding: 32px; border: 3px dashed rgba(255,255,255,0.4); border-radius: 20px; background: rgba(255,255,255,0.1); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; transition: all 0.3s ease;" id="dropZone">
                        <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.8;">📄</div>
                        <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px;">Drag & Drop PDF Here</div>
                        <div style="font-size: 14px; color: rgba(255,255,255,0.7);">or click to browse files</div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 24px;">
                    <button onclick="uploadPDF()" style="background:#ff8533; color:white; flex: 1;">🤖 AI Analysis</button>
                    <button onclick="showAuditLog()" style="background:rgba(255,255,255,0.2); color:white; flex: 1;">📈 Audit Log</button>
                </div>
            </div>
            </div>
            
            <div class="hero" style="grid-column: 1 / -1;" id="documentHistory"></div>
        </div>

        <div id="result"></div>
    </div>
    

    
    <script>
        function logout() {
            if(confirm('Are you sure you want to logout?')) {
                window.location.href = './index.html';
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
        
        // File input change handler
        document.getElementById('pdfFile').addEventListener('change', function(e) {
            const dropZone = document.getElementById('dropZone');
            if (e.target.files.length > 0) {
                const fileName = e.target.files[0].name;
                dropZone.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 16px; color: #4ade80;">✅</div>
                    <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px;">File Selected</div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.9); font-weight: 500;">${fileName}</div>
                `;
                dropZone.style.borderColor = 'rgba(74, 222, 128, 0.6)';
                dropZone.style.background = 'rgba(74, 222, 128, 0.1)';
            } else {
                dropZone.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 16px; opacity: 0.8;">📄</div>
                    <div style="font-size: 18px; font-weight: 700; color: white; margin-bottom: 8px;">Drag & Drop PDF Here</div>
                    <div style="font-size: 14px; color: rgba(255,255,255,0.7);">or click to browse files</div>
                `;
                dropZone.style.borderColor = 'rgba(255,255,255,0.4)';
                dropZone.style.background = 'rgba(255,255,255,0.1)';
            }
        });
        

    </script>

    <script>
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
        
        function showDocDetails() {
            showModal('📄 Document Details', '<p>Document processed successfully</p>');
        }
        
        async function showDocumentDetailsFromBelow(index) {
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
                            const priorityColors = {'critical': '#dc3545', 'high': '#fd7e14', 'normal': '#28a745', 'low': '#6c757d'};
                            html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                            html += `<strong>📚 ${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                            html += `👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}<br>`;
                            html += `🎯 Priority: ${assignment.priority} | ⏰ ${new Date(assignment.timestamp).toLocaleString()}`;
                            if (assignment.reason) html += `<br>📝 ${assignment.reason}`;
                            html += `</div>`;
                        });
                    } else {
                        html += '<p>No course assignments</p>';
                    }
                    
                    if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                        html += `<h5>⚠️ Skipped Duplicates:</h5>`;
                        doc.skipped_duplicates.forEach(skip => {
                            html += `<div style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                            html += `<strong>😫 ${skip.name}</strong> (${skip.user_id})<br>`;
                            html += `<div style="margin: 4px 0; color: #856404;"><strong>Skipped:</strong> ${skip.skipped_courses.join(', ')}</div>`;
                            html += `<div style="color: #856404; font-style: italic;">${skip.reason}</div>`;
                            html += `</div>`;
                        });
                    }
                    
                    document.getElementById('modalBody').innerHTML = html;
                } else {
                    document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Document not found</div>';
                }
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading document details</div>';
            }
        }
        
        async function loadDocumentHistoryModal() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                let html = `<h4>📄 История документов (${data.total_documents})</h4>`;
                
                if (data.documents && data.documents.length > 0) {
                    html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                        <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                        <select onchange="sortDocuments(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                            <option value="date">По дате</option>
                            <option value="title">По названию</option>
                            <option value="assignments">По назначениям</option>
                        </select>
                    </div>`;
                    html += `<div id="documentsList">`;
                    
                    data.documents.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div class="document-item" data-date="${doc.processed_at}" data-title="${doc.title}" data-assignments="${doc.assignments_count}" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                        html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
                        html += `<strong style="font-size: 18px; color: #2a7d2e;">📄 ${doc.title}</strong>`;
                        html += `<button onclick="toggleDetailsModal('doc${index}')" style="background: #007bff; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px;">🔍 Подробности</button>`;
                        html += `</div>`;
                        html += `<div style="color: #6c757d; font-size: 14px;">⏰ ${date} | 🎯 ${doc.assignments_count} назначений</div>`;
                        
                        // Скрытые детали
                        html += `<div id="doc${index}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #dee2e6;">`;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5>📈 Назначения курсов:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                                html += `<strong style="color: #2a7d2e;">📚 ${assignment.course_id}</strong> → ${assignment.user_name || assignment.user_id}<br>`;
                                html += `<div style="margin: 4px 0; color: #666; font-size: 13px;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                                html += `<div style="color: #666; font-size: 13px;">🎯 Приоритет: ${assignment.priority} | ⏰ ${assignDate}</div>`;
                                if (assignment.reason) html += `<div style="margin-top: 4px; color: #666; font-size: 13px;">📝 ${assignment.reason}</div>`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic;">Никому не назначались курсы</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5>⚠️ Пропущено дубликатов:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                                html += `<strong>😫 ${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<div style="margin: 4px 0; color: #856404;"><strong>Пропущено:</strong> ${skip.skipped_courses.join(', ')}</div>`;
                                html += `<div style="color: #856404; font-style: italic;">${skip.reason}</div>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div></div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #6c757d;">Нет обработанных документов</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error loading document history:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки истории</div>';
            }
        }
        
        function toggleDetailsModal(id) {
            const element = document.getElementById(id);
            if (element.style.display === 'none') {
                element.style.display = 'block';
            } else {
                element.style.display = 'none';
            }
        }
        
        async function checkExpiredModal() {
            try {
                const response = await fetch('/expired-courses');
                const data = await response.json();
                
                let html = `<h4>⏰ Проверка сроков курсов</h4>`;
                
                if (data.expired_users && data.expired_users.length > 0) {
                    html += `<h5>⚠️ Найдено ${data.expired_count} пользователей с истекающими курсами:</h5>`;
                    
                    data.expired_users.forEach(user => {
                        html += `<div style="background: #fff3cd; padding: 16px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #ffc107;">`;
                        html += `<strong style="font-size: 18px; color: #856404;">${user.user_name || user.user_id}</strong> - ${user.role || ''}, ${user.department || ''}<br>`;
                        html += `<div style="margin: 12px 0;"><strong>Истекающие курсы:</strong></div>`;
                        
                        user.expired_courses.forEach(course => {
                            html += `<div style="margin: 8px 0; padding: 8px; background: #f8d7da; border-radius: 6px;">`;
                            html += `<strong style="color: #721c24;">🚨 ${course.course_id}</strong><br>`;
                            html += `<div style="color: #721c24; font-size: 13px;">Назначен: ${new Date(course.assigned_at).toLocaleDateString()} | Период: ${course.period_months} месяцев</div>`;
                            html += `</div>`;
                        });
                        
                        html += `</div>`;
                    });
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #28a745;">✅ Все курсы актуальны!</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка проверки сроков</div>';
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                // Обновляем карточки статистики
                document.getElementById('userCount').textContent = data.users;
                document.getElementById('courseCount').textContent = data.courses;
                document.getElementById('assignmentCount').textContent = data.assignments;
                document.getElementById('documentCount').textContent = data.documents;
                document.getElementById('completionCount').textContent = data.completions || 0;
                document.getElementById('expiredCount').textContent = data.expired || 0;
                document.getElementById('criticalCount').textContent = data.critical || 0;
                document.getElementById('activeCount').textContent = data.active || 0;
                
                // Обновляем прогресс бар
                const totalAssignments = data.assignments || 0;
                const completedAssignments = data.completions || 0;
                const progressPercent = totalAssignments > 0 ? Math.round((completedAssignments / totalAssignments) * 100) : 0;
                
                document.getElementById('progressPercent').textContent = progressPercent + '%';
                document.getElementById('progressFill').style.width = progressPercent + '%';
                document.getElementById('completedCount').textContent = completedAssignments;
                document.getElementById('totalAssignments').textContent = totalAssignments;
                document.getElementById('activeUsers').textContent = data.users || 0;
                
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function showUsers() {
            showModal('👥 Users', '<div style="text-align: center; padding: 40px;">👥 Loading users list...</div>');
            
            try {
                const response = await fetch('/users-detail');
                const data = await response.json();
                
                let html = `<h4>👥 Users (${data.users.length})</h4>`;
                html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                    <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Sort by:</label>
                    <select onchange="sortUsers(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <option value="name">By Name</option>
                        <option value="role">By Role</option>
                        <option value="department">By Department</option>
                        <option value="assignments">By Assignments</option>
                    </select>
                </div>`;
                html += `<div id="usersList">`;
                
                data.users.forEach(user => {
                    const lastAssignment = user.latest_assignment ? new Date(user.latest_assignment).toLocaleDateString() : 'Never';
                    
                    html += `<div class="user-item" data-name="${user.name}" data-role="${user.role}" data-department="${user.department}" data-assignments="${user.assignments_count}" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                    html += `<strong onclick="showUserProfile('${user.user_id}')" style="color: #2a7d2e; cursor: pointer; text-decoration: underline; font-size: 18px;">👤 ${user.name}</strong> (${user.user_id})<br>`;
                    html += `<div style="margin: 8px 0; color: #666;">🏢 ${user.role} | ${user.department}</div>`;
                    html += `<div style="color: #666;">🎯 Assignments: ${user.assignments_count} | Last: ${lastAssignment}</div>`;
                    html += `</div>`;
                });
                
                html += `</div>`;
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading users</div>';
            }
        }
        
        async function showCourses() {
            showModal('📚 Courses', '<div style="text-align: center; padding: 40px;">📚 Loading courses list...</div>');
            
            try {
                const response = await fetch('/courses-detail');
                const data = await response.json();
                
                let html = `<h4>📚 Courses (${data.courses.length})</h4>`;
                html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                    <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                    <select onchange="sortCourses(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <option value="name">По названию</option>
                        <option value="assignments">По назначениям</option>
                        <option value="category">По категории</option>
                        <option value="priority">По приоритету</option>
                    </select>
                </div>`;
                html += `<div id="coursesList">`;
                
                data.courses.forEach(course => {
                    const lastAssignment = course.latest_assignment ? new Date(course.latest_assignment).toLocaleDateString() : 'Никогда';
                    
                    html += `<div class="course-item" data-name="${course.course_name || course.course_id}" data-assignments="${course.assignments_count}" data-category="${course.category || ''}" data-priority="${course.priority}" style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                    html += `<strong style="font-size: 18px; color: #2a7d2e;">📚 ${course.course_name || course.course_id}</strong> (${course.course_id})<br>`;
                    html += `<div style="margin: 8px 0; color: #666;">📝 ${course.description || ''}</div>`;
                    html += `<div style="color: #666;">🎯 Назначений: ${course.assignments_count} | Последнее: ${lastAssignment}</div>`;
                    html += `<div style="color: #666;">🔄 Период: ${course.renewal_months} мес. | Приоритет: ${course.priority}</div>`;
                    html += `</div>`;
                });
                
                html += `</div>`;
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Error loading courses</div>';
            }
        }
        
        async function showAssignments() {
            showModal('🎯 Assignments', '<div style="text-align: center; padding: 40px;">🎯 Loading assignments...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                let html = `<h4>🎯 Recent Assignments (${data.assignments.length})</h4>`;
                html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                    <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                    <select onchange="sortAssignments(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <option value="date">По дате</option>
                        <option value="priority">По приоритету</option>
                        <option value="course">По курсу</option>
                        <option value="user">По пользователю</option>
                    </select>
                </div>`;
                html += `<div id="assignmentsList">`;
                
                data.assignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div class="assignment-item" data-date="${assignment.timestamp}" data-priority="${assignment.priority}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                    html += `<strong style="font-size: 18px; color: #2a7d2e;">📚 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                    html += `<div style="margin: 8px 0; color: #666;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                    html += `<div style="color: #666;">🎯 Приоритет: ${assignment.priority} | ⏰ ${date}</div>`;
                    if (assignment.reason) html += `<div style="margin-top: 8px; color: #666;">📝 ${assignment.reason}</div>`;
                    html += `</div>`;
                });
                
                html += `</div>`;
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки назначений</div>';
            }
        }
        
        async function showDocuments() {
            showModal('📄 Documents', '<div style="text-align: center; padding: 40px;">📄 Loading document history...</div>');
            loadDocumentHistoryModal();
        }
        
        function sortDocuments(sortBy) {
            const container = document.getElementById('documentsList');
            if (!container) return;
            
            const items = Array.from(container.querySelectorAll('.document-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        async function showExpired() {
            showModal('❌ Expired', '<div style="text-align: center; padding: 40px;">❌ Checking expired courses...</div>');
            checkExpiredModal();
        }
        
        async function showCritical() {
            showModal('🔴 Critical', '<div style="text-align: center; padding: 40px;">🔴 Loading critical courses...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                const criticalAssignments = data.assignments.filter(a => a.priority === 'critical');
                
                let html = `<h4>🔴 Критичные курсы (${criticalAssignments.length})</h4>`;
                
                if (criticalAssignments.length > 0) {
                    html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                        <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                        <select onchange="sortCritical(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                            <option value="date">По дате</option>
                            <option value="course">По курсу</option>
                            <option value="user">По пользователю</option>
                        </select>
                    </div>`;
                    html += `<div id="criticalList">`;
                    
                    criticalAssignments.forEach(assignment => {
                        const date = new Date(assignment.timestamp).toLocaleString();
                        
                        html += `<div class="critical-item" data-date="${assignment.timestamp}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" style="background: #fff3cd; border-left: 4px solid #dc3545; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                        html += `<strong style="font-size: 18px; color: #dc3545;">🔴 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                        html += `<div style="margin: 8px 0; color: #666;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                        html += `<div style="color: #666;">⏰ Назначен: ${date}</div>`;
                        if (assignment.reason) html += `<div style="margin-top: 8px; color: #666;">📝 ${assignment.reason}</div>`;
                        html += `</div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #6c757d;">Нет критичных курсов</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки критичных курсов</div>';
            }
        }
        
        async function showActive() {
            showModal('⚙️ Active', '<div style="text-align: center; padding: 40px;">⚙️ Loading active courses...</div>');
            
            try {
                const response = await fetch('/assignments-detail');
                const data = await response.json();
                
                let html = `<h4>⚙️ Активные курсы (в процессе)</h4>`;
                html += '<p style="color: #666; margin-bottom: 20px;">Показываем курсы, которые назначены, но еще не завершены и не просрочены</p>';
                html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                    <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                    <select onchange="sortActive(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <option value="date">По дате</option>
                        <option value="priority">По приоритету</option>
                        <option value="course">По курсу</option>
                        <option value="user">По пользователю</option>
                    </select>
                </div>`;
                html += `<div id="activeList">`;
                
                data.assignments.forEach(assignment => {
                    const date = new Date(assignment.timestamp).toLocaleString();
                    const priorityColors = {
                        'critical': '#dc3545',
                        'high': '#fd7e14', 
                        'normal': '#28a745',
                        'low': '#6c757d'
                    };
                    
                    html += `<div class="active-item" data-date="${assignment.timestamp}" data-priority="${assignment.priority}" data-course="${assignment.course_id}" data-user="${assignment.user_name || assignment.user_id}" style="background: #f8f9fa; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                    html += `<strong style="font-size: 18px; color: #2a7d2e;">⚙️ ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                    html += `<div style="margin: 8px 0; color: #666;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                    html += `<div style="color: #666;">🎯 Приоритет: ${assignment.priority} | ⏰ ${date}</div>`;
                    if (assignment.reason) html += `<div style="margin-top: 8px; color: #666;">📝 ${assignment.reason}</div>`;
                    html += `</div>`;
                });
                
                html += `</div>`;
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки активных курсов</div>';
            }
        }
        
        async function showCompletions() {
            showModal('✅ Completed', '<div style="text-align: center; padding: 40px;">✅ Loading completed courses...</div>');
            
            try {
                const response = await fetch('/completions-detail');
                const data = await response.json();
                
                let html = `<h4>✅ Завершенные курсы (${data.completions.length})</h4>`;
                
                if (data.completions && data.completions.length > 0) {
                    html += `<div style="margin: 16px 0; padding: 12px; background: var(--system-fill); border-radius: 12px;">
                        <label style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 600; color: var(--label-primary); margin-right: 8px;">Сортировка:</label>
                        <select onchange="sortCompletions(this.value)" style="padding: 8px 12px; border-radius: 8px; border: none; background: var(--system-background); color: var(--label-primary); font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif; font-weight: 500; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                            <option value="date">По дате завершения</option>
                            <option value="course">По курсу</option>
                            <option value="user">По пользователю</option>
                            <option value="method">По методу</option>
                        </select>
                    </div>`;
                    html += `<div id="completionsList">`;
                    
                    data.completions.forEach(completion => {
                        const date = new Date(completion.completed_at).toLocaleString();
                        
                        html += `<div class="completion-item" data-date="${completion.completed_at}" data-course="${completion.course_id}" data-user="${completion.user_name || completion.user_id}" data-method="${completion.completion_method}" style="background: #d4edda; border-left: 4px solid #28a745; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                        html += `<strong style="font-size: 18px; color: #28a745;">✅ ${completion.course_id}</strong> → <strong onclick="showUserProfile('${completion.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${completion.user_name || completion.user_id}</strong><br>`;
                        html += `<div style="margin: 8px 0; color: #666;">👤 ${completion.user_role || ''}, ${completion.user_department || ''}</div>`;
                        html += `<div style="color: #666;">⏰ Завершен: ${date} | 🎯 Метод: ${completion.completion_method}</div>`;
                        html += `</div>`;
                    });
                    
                    html += `</div>`;
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #6c757d;">Никто еще не завершил курсы</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
            } catch (error) {
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки завершений</div>';
            }
        }
        
        async function showUserProfile(userId) {
            showModal('👤 Профиль пользователя', '<div style="text-align: center; padding: 40px;">👤 Загружаю профиль...</div>');
            
            try {
                const response = await fetch(`/user/${userId}`);
                const data = await response.json();
                
                if (data.error) {
                    document.getElementById('modalBody').innerHTML = `<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ ${data.error}</div>`;
                    return;
                }
                
                let html = '<div>';
                html += `<h3>👤 Профиль пользователя</h3>`;
                
                // Основная информация
                html += `<div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">`;
                html += `<h4>👤 ${data.user.name} (${data.user.user_id})</h4>`;
                html += `<p><strong>🏢 Должность:</strong> ${data.user.role}</p>`;
                html += `<p><strong>🏭 Отдел:</strong> ${data.user.department}</p>`;

                
                // Добавляем детальную статистику
                const completedCount = data.assignments.filter(a => a.is_completed).length;
                const expiredCount = data.assignments.filter(a => a.is_expired && !a.is_completed).length;
                const criticalCount = data.assignments.filter(a => a.priority === 'critical' && !a.is_completed).length;
                const highCount = data.assignments.filter(a => a.priority === 'high' && !a.is_completed).length;
                const normalCount = data.assignments.filter(a => a.priority === 'normal' && !a.is_completed).length;
                const lowCount = data.assignments.filter(a => a.priority === 'low' && !a.is_completed).length;
                const urgentDeadlines = data.assignments.filter(a => {
                    if (a.is_completed || a.is_expired) return false;
                    const assignedDate = new Date(a.timestamp);
                    const deadlineDays = a.deadline_days || 30;
                    const deadlineDate = new Date(assignedDate.getTime() + deadlineDays * 24 * 60 * 60 * 1000);
                    const daysLeft = Math.ceil((deadlineDate - new Date()) / (1000 * 60 * 60 * 24));
                    return daysLeft <= 7;
                }).length;
                
                html += `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin: 15px 0;">`;
                html += `<div style="background: #d4edda; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${data.active_courses}</strong><br><small>✅ Активных</small></div>`;
                html += `<div style="background: #cce5ff; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${completedCount}</strong><br><small>✅ Завершено</small></div>`;
                html += `<div style="background: #ffebee; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${urgentDeadlines}</strong><br><small>⚠️ Скоро дедлайн</small></div>`;
                html += `<div style="background: #f8d7da; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${expiredCount}</strong><br><small>❌ Просрочено</small></div>`;
                html += `<div style="background: #e3f2fd; padding: 8px 12px; border-radius: 5px; text-align: center;"><strong>${data.total_assignments}</strong><br><small>📚 Всего</small></div>`;
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
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: var(--gray-600);">❌ Ошибка загрузки профиля</div>';
            }
        }
        
        // Загружаем статистику и историю при загрузке страницы
        window.onload = function() {
            loadStats();
            loadDocumentHistoryBelow();
        }
        
        let documentsDisplayed = 5; // Показываем первые 5 документов
        let allDocuments = []; // Храним все документы
        
        async function loadDocumentHistoryBelow() {
            try {
                const response = await fetch('/document-history');
                const data = await response.json();
                
                const historyDiv = document.getElementById('documentHistory');
                allDocuments = data.documents || [];
                
                if (allDocuments.length > 0) {
                    renderDocuments();
                } else {
                    historyDiv.innerHTML = '<h1>📄 Processed Documents</h1><div style="text-align: center; padding: var(--space-xxl) var(--space-l);"><div style="font-size: var(--text-xxl); margin-bottom: var(--space-m); opacity: 0.5;">📚</div><h3>No processed documents</h3><p>Upload your first PDF protocol for analysis!</p></div>';
                }
                
            } catch (error) {
                console.error('Error loading document history:', error);
            }
        }
        
        function renderDocuments() {
            const historyDiv = document.getElementById('documentHistory');
            
            // Применяем фильтры
            let filteredDocuments = [...allDocuments];
            const sortBy = document.getElementById('sortFilter')?.value || 'date';
            const filterBy = document.getElementById('assignmentFilter')?.value || 'all';

            
            // Фильтрация
            if (filterBy === 'with-assignments') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count > 0);
            }
            if (filterBy === 'no-assignments') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count === 0);
            }
            if (filterBy === 'high-impact') {
                filteredDocuments = filteredDocuments.filter(doc => doc.assignments_count >= 5);
            }
            if (filterBy === 'recent') {
                const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
                filteredDocuments = filteredDocuments.filter(doc => new Date(doc.processed_at) > weekAgo);
            }
            if (filterBy === 'safety') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('safety') || 
                    doc.title.toLowerCase().includes('безопасность') ||
                    doc.title.toLowerCase().includes('охрана')
                );
            }
            if (filterBy === 'training') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('training') || 
                    doc.title.toLowerCase().includes('обучение') ||
                    doc.title.toLowerCase().includes('курс')
                );
            }
            if (filterBy === 'incident') {
                filteredDocuments = filteredDocuments.filter(doc => 
                    doc.title.toLowerCase().includes('incident') || 
                    doc.title.toLowerCase().includes('инцидент') ||
                    doc.title.toLowerCase().includes('происшествие') ||
                    doc.title.toLowerCase().includes('нарушение')
                );
            }
            

            
            // Сортировка после всех фильтров
            filteredDocuments.sort((a, b) => {
                if (sortBy === 'date') {
                    return new Date(b.processed_at) - new Date(a.processed_at);
                }
                if (sortBy === 'assignments') {
                    return b.assignments_count - a.assignments_count;
                }
                if (sortBy === 'impact') {
                    const aImpact = a.assignments_count + (a.skipped_duplicates?.length || 0);
                    const bImpact = b.assignments_count + (b.skipped_duplicates?.length || 0);
                    return bImpact - aImpact;
                }
                if (sortBy === 'alphabetical') {
                    return a.title.localeCompare(b.title);
                }
                return 0;
            });
            
            const documentsToShow = filteredDocuments.slice(0, documentsDisplayed);
            
            let html = '<h1>📄 Processed Documents (' + allDocuments.length + ')</h1>';
            
            // Добавляем фильтры
            html += '<div style="background: rgba(255,255,255,0.2); padding: 16px; border-radius: 12px; margin-bottom: 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">';
            html += '<div style="display: flex; align-items: center; gap: 8px;">';
            html += '<label style="font-weight: 600; color: var(--gray-800);">Sort:</label>';
            html += '<select id="sortFilter" onchange="renderDocuments()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(0,0,0,0.2); background: white;">';
            html += '<option value="date"' + (sortBy === 'date' ? ' selected' : '') + '>By Date (Newest)</option>';
            html += '<option value="assignments"' + (sortBy === 'assignments' ? ' selected' : '') + '>By Assignments (Most)</option>';
            html += '<option value="impact"' + (sortBy === 'impact' ? ' selected' : '') + '>By Impact (Assignments + Skipped)</option>';
            html += '<option value="alphabetical"' + (sortBy === 'alphabetical' ? ' selected' : '') + '>Alphabetical (A-Z)</option>';
            html += '</select>';
            html += '</div>';

            
            html += '<div style="display: flex; align-items: center; gap: 8px;">';
            html += '<label style="font-weight: 600; color: var(--gray-800);">Filter:</label>';
            html += '<select id="assignmentFilter" onchange="resetAndFilter()" style="padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(0,0,0,0.2); background: white;">';
            html += '<option value="all"' + (filterBy === 'all' ? ' selected' : '') + '>All Documents</option>';
            html += '<option value="with-assignments"' + (filterBy === 'with-assignments' ? ' selected' : '') + '>With Assignments</option>';
            html += '<option value="no-assignments"' + (filterBy === 'no-assignments' ? ' selected' : '') + '>No Assignments</option>';
            html += '<option value="high-impact"' + (filterBy === 'high-impact' ? ' selected' : '') + '>High Impact (5+ assignments)</option>';
            html += '<option value="recent"' + (filterBy === 'recent' ? ' selected' : '') + '>Recent (Last 7 days)</option>';
            html += '<option value="safety"' + (filterBy === 'safety' ? ' selected' : '') + '>Safety Related</option>';
            html += '<option value="training"' + (filterBy === 'training' ? ' selected' : '') + '>Training Related</option>';
            html += '<option value="incident"' + (filterBy === 'incident' ? ' selected' : '') + '>Incident Reports</option>';
            html += '</select>';
            html += '</div>';

            html += '<div style="color: var(--gray-600); font-size: 14px;">Showing ' + documentsToShow.length + ' of ' + filteredDocuments.length + ' documents</div>';
            html += '</div>';
            
            html += '<div>';
            
            documentsToShow.forEach((doc, index) => {
                        const date = new Date(doc.processed_at).toLocaleString();
                        
                        html += `<div class="training-card full-training">`;
                        
                        html += `<div class="training-content">`;
                        html += `<h3 class="training-title">`;
                        html += `<span class="training-icon">📄</span>`;
                        html += `${doc.title}`;
                        html += `</h3>`;
                        html += `<p class="training-desc">Обработан ${date}</p>`;
                        html += `<div class="training-meta">`;
                        html += `<span>Type: Протокол</span>`;
                        html += `<span>🎯 ${doc.assignments_count} назначений</span>`;
                        html += `<span>Status: Обработан</span>`;
                        html += `</div>`;
                        html += `</div>`;
                        
                        html += `<div class="training-action">`;
                        html += `<button class="training-btn" onclick="showDocumentDetailsFromBelow(${index})">Details</button>`;
                        html += `</div>`;
                        
                        html += `</div>`;
                        
                        // Скрытые детали
                        html += `<div id="docBelow${index}" style="display: none; margin-top: 15px; padding: 20px; background: #f8f9fa; border-radius: 16px; border-left: 4px solid #2a7d2e;">`;;
                        
                        if (doc.assignments && doc.assignments.length > 0) {
                            html += `<h5 style="font-size: 18px; font-weight: 700; margin-bottom: 16px; color: #2a7d2e;">📊 Назначения курсов:</h5>`;
                            
                            doc.assignments.forEach(assignment => {
                                const assignDate = new Date(assignment.timestamp).toLocaleString();
                                const priorityColors = {
                                    'critical': '#dc3545',
                                    'high': '#fd7e14', 
                                    'normal': '#28a745',
                                    'low': '#6c757d'
                                };
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[assignment.priority] || '#28a745'}; padding: 12px; margin: 8px 0; border-radius: 12px; font-size: 14px; box-shadow: var(--ehs-shadow);">`;
                                html += `<strong style="color: #2a7d2e;">📚 ${assignment.course_id}</strong> → <strong onclick="showUserProfile('${assignment.user_id}')" style="color: #007bff; cursor: pointer; text-decoration: underline;">${assignment.user_name || assignment.user_id}</strong><br>`;
                                html += `<div style="margin: 4px 0; color: #666;">👤 ${assignment.user_role || ''}, ${assignment.user_department || ''}</div>`;
                                html += `<div style="color: #666;">🎯 Приоритет: ${assignment.priority} | ⏰ ${assignDate}</div>`;
                                if (assignment.reason) html += `<div style="margin-top: 4px; color: #666; font-style: italic;">📝 ${assignment.reason}</div>`;
                                html += `</div>`;
                            });
                        } else {
                            html += '<p style="color: #6c757d; font-style: italic; text-align: center; padding: 20px;">Никому не назначались курсы</p>';
                        }
                        
                        // Показываем пропущенные дубликаты
                        if (doc.skipped_duplicates && doc.skipped_duplicates.length > 0) {
                            html += `<h5 style="font-size: 18px; font-weight: 700; margin: 16px 0; color: #f59e0b;">⚠️ Пропущено дубликатов:</h5>`;
                            doc.skipped_duplicates.forEach(skip => {
                                html += `<div style="background: #fff3cd; padding: 12px; margin: 8px 0; border-radius: 12px; border-left: 4px solid #ffc107; box-shadow: var(--ehs-shadow);">`;
                                html += `<strong onclick="showUserProfile('${skip.user_id}')" style="color: #856404; cursor: pointer; text-decoration: underline;">😫 ${skip.name}</strong> (${skip.user_id})<br>`;
                                html += `<div style="margin: 4px 0; color: #856404;"><strong>Пропущено:</strong> ${skip.skipped_courses.join(', ')}</div>`;
                                html += `<div style="color: #856404; font-style: italic;">${skip.reason}</div>`;
                                html += `</div>`;
                            });
                        }
                        
                        html += `</div>`;
                        

                    });
                    
                    html += '</div>';
                    
                    // Добавляем кнопку "Load More" если есть еще документы
                    if (documentsDisplayed < filteredDocuments.length) {
                        html += '<div style="text-align: center; margin-top: 20px;">';
                        html += '<button onclick="loadMoreDocuments()" style="background: var(--brand); color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">Load More (' + (filteredDocuments.length - documentsDisplayed) + ' remaining)</button>';
                        html += '</div>';
                    }
                    
                    historyDiv.innerHTML = html;
        }
        
        function loadMoreDocuments() {
            documentsDisplayed += 10; // Загружаем еще 10 документов
            renderDocuments();
        }
        
        function resetAndFilter() {
            documentsDisplayed = 5; // Сбрасываем к первым 5 документам
            renderDocuments();
        }

        function displayResult(data) {
            let html = '';
            let title = '';
            
            // Проверяем, является ли документ дубликатом
            if (data.is_duplicate) {
                title = '⚠️ Документ уже обрабатывался';
                html += '<h4>⚠️ Документ уже обрабатывался!</h4>';
                html += `<div style="background: #fff3cd; padding: 16px; border-radius: 8px; margin: 16px 0;">`;
                html += `<div style="margin: 8px 0;"><strong>Предыдущая обработка:</strong> ${data.previous_processing.processed_at}</div>`;
                html += `<div style="margin: 8px 0;"><strong>Назначений тогда:</strong> ${data.previous_processing.assignments_count}</div>`;
                html += `<div style="margin: 8px 0;"><strong>Пользователи:</strong> ${data.previous_processing.assigned_users.join(', ')}</div>`;
                html += `</div>`;
                
                if (data.extracted_text) {
                    html += `<div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin: 16px 0;">`;
                    html += `<strong>Протокол:</strong><br>${data.extracted_text}`;
                    html += `</div>`;
                }
            } else {
                title = `✅ AI анализ завершен`;
                html += `<h4>✅ AI анализ завершен для ${data.total_users} пользователей</h4>`;
                
                if (data.extracted_text) {
                    html += `<div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin: 16px 0;">`;
                    html += `<strong>Протокол:</strong><br>${data.extracted_text}`;
                    html += `</div>`;
                }
                
                if (data.assignments && data.assignments.length > 0) {
                    html += `<h5>🎯 AI назначил курсы (${data.assignments.length} пользователей):</h5>`;
                    
                    data.assignments.forEach(assignment => {
                        html += `<div style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 16px; margin: 12px 0;">`;
                        html += `<strong style="font-size: 18px; color: #2a7d2e;">${assignment.name}</strong> (${assignment.user_id}) - ${assignment.role}, ${assignment.department}<br>`;
                        html += `<div style="margin: 12px 0;"><strong>Курсы с AI-определенными сроками:</strong></div>`;
                        assignment.courses_assigned.forEach(courseId => {
                            html += `<span style="background: #e8f5e8; padding: 6px 12px; margin: 4px; border-radius: 6px; display: inline-block;">📚 ${courseId}</span> `;
                        });
                        if (assignment.reason) {
                            html += `<div style="margin: 12px 0; font-style: italic; color: #666;">AI обоснование: ${assignment.reason}</div>`;
                        }
                        if (assignment.course_periods) {
                            html += `<div style="margin: 12px 0;"><strong>🔄 AI определил:</strong></div>`;
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
                                
                                html += `<div style="background: white; border-left: 4px solid ${priorityColors[period.priority] || '#17a2b8'}; padding: 12px; margin: 8px 0; border-radius: 6px;">`;
                                html += `<strong>📚 ${period.course_id}</strong><br>`;
                                html += `<div style="margin: 4px 0; color: #666;">🎯 Приоритет: ${priorityNames[period.priority] || period.priority}</div>`;
                                html += `<div style="color: #666;">🔄 Периодичность: каждые ${period.months} мес. | ⏰ Дедлайн: ${period.deadline_days} дней</div>`;
                                html += `</div>`;
                            });
                        }
                        html += `</div>`;
                    });
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #666;">AI определил: никому не нужны новые курсы по этому протоколу</div>';
                }
                
                // Показываем пропущенные дубликаты
                if (data.skipped_duplicates && data.skipped_duplicates.length > 0) {
                    html += `<h5>⚠️ Пропущено дубликатов (${data.skipped_duplicates.length} пользователей):</h5>`;
                    
                    data.skipped_duplicates.forEach(skip => {
                        html += `<div style="background: #fff3cd; padding: 16px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #ffc107;">`;
                        html += `<strong>${skip.name}</strong> (${skip.user_id})<br>`;
                        html += `<div style="margin: 8px 0;"><strong>Пропущено:</strong></div>`;
                        skip.skipped_courses.forEach(courseId => {
                            html += `<span style="background: #f8d7da; padding: 4px 8px; margin: 2px; border-radius: 3px; display: inline-block;">🚫 ${courseId}</span> `;
                        });
                        html += `<div style="margin-top: 8px; font-style: italic; color: #856404;">${skip.reason}</div>`;
                        html += `</div>`;
                    });
                }
                
                // Показываем пропущенные дубликаты
                if (data.skipped_duplicates && data.skipped_duplicates.length > 0) {
                    html += `<h5>⚠️ Пропущено дубликатов (${data.skipped_duplicates.length} пользователей):</h5>`;
                    
                    data.skipped_duplicates.forEach(skip => {
                        html += `<div style="background: #fff3cd; padding: 16px; margin: 12px 0; border-radius: 8px; border-left: 4px solid #ffc107;">`;
                        html += `<strong>${skip.name}</strong> (${skip.user_id})<br>`;
                        html += `<div style="margin: 8px 0;"><strong>Пропущено:</strong></div>`;
                        skip.skipped_courses.forEach(courseId => {
                            html += `<span style="background: #f8d7da; padding: 4px 8px; margin: 2px; border-radius: 3px; display: inline-block;">🚫 ${courseId}</span> `;
                        });
                        html += `<div style="margin-top: 8px; font-style: italic; color: #856404;">${skip.reason}</div>`;
                        html += `</div>`;
                    });
                }
            }
            
            showModal(title, html);
            
            // Обновляем статистику и историю
            loadStats();
            loadDocumentHistoryBelow();
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
            showModal('📈 Audit Log', '<div style="text-align: center; padding: 40px;">📈 Loading audit log...</div>');
            
            try {
                const response = await fetch('/audit-log');
                const data = await response.json();
                
                let html = `<h4>📈 Audit Log - Последние ${data.total_logs} действий</h4>`;
                
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
                            
                            html += `<div style="background: #f8f9fa; border-left: 4px solid ${priorityColors[log.priority] || '#28a745'}; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                            html += `<strong style="font-size: 16px; color: #2a7d2e;">📚 Курс назначен:</strong> ${log.course_id}<br>`;
                            html += `<div style="margin: 8px 0; color: #666;">👤 <strong>Пользователь:</strong> ${log.user_name || log.user_id} (${log.user_role || ''}, ${log.user_department || ''})</div>`;
                            html += `<div style="color: #666;">🤖 <strong>Назначил:</strong> ${log.assigned_by} | 🎯 <strong>Приоритет:</strong> ${log.priority}</div>`;
                            if (log.reason) html += `<div style="margin-top: 8px; color: #666;">📝 <strong>Причина:</strong> ${log.reason}</div>`;
                            html += `<div style="margin-top: 8px; color: #666;">⏰ <strong>Время:</strong> ${date}</div>`;
                            html += `</div>`;
                        } else if (log.action === 'document_processed') {
                            html += `<div style="background: #e7f3ff; border-left: 4px solid #007bff; padding: 16px; margin: 12px 0; border-radius: 8px;">`;
                            html += `<strong style="font-size: 16px; color: #007bff;">📄 Документ обработан</strong><br>`;
                            html += `<div style="margin: 8px 0; color: #666;">📝 <strong>Протокол:</strong> ${log.protocol_title}</div>`;
                            html += `<div style="color: #666;">🎯 <strong>Назначений:</strong> ${log.assignments_count} | ⏰ <strong>Время:</strong> ${date}</div>`;
                            html += `</div>`;
                        }
                    });
                } else {
                    html += '<div style="text-align: center; padding: 40px; color: #6c757d;">ℹ️ Лог пуст</div>';
                }
                
                document.getElementById('modalBody').innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('modalBody').innerHTML = '<div style="text-align: center; padding: 40px; color: #dc3545;">❌ Ошибка загрузки audit log</div>';
            }
        }
        
        // Функции сортировки
        function sortUsers(sortBy) {
            const container = document.getElementById('usersList');
            const items = Array.from(container.querySelectorAll('.user-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal); // По убыванию для чисел
                }
                return aVal.localeCompare(bVal); // По алфавиту
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortCourses(sortBy) {
            const container = document.getElementById('coursesList');
            const items = Array.from(container.querySelectorAll('.course-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'assignments') {
                    return parseInt(bVal) - parseInt(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortAssignments(sortBy) {
            const container = document.getElementById('assignmentsList');
            const items = Array.from(container.querySelectorAll('.assignment-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal); // Новые сверху
                }
                if (sortBy === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[bVal] || 0) - (priorities[aVal] || 0);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortCompletions(sortBy) {
            const container = document.getElementById('completionsList');
            const items = Array.from(container.querySelectorAll('.completion-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortCritical(sortBy) {
            const container = document.getElementById('criticalList');
            const items = Array.from(container.querySelectorAll('.critical-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
        
        function sortActive(sortBy) {
            const container = document.getElementById('activeList');
            const items = Array.from(container.querySelectorAll('.active-item'));
            
            items.sort((a, b) => {
                let aVal = a.dataset[sortBy] || '';
                let bVal = b.dataset[sortBy] || '';
                
                if (sortBy === 'date') {
                    return new Date(bVal) - new Date(aVal);
                }
                if (sortBy === 'priority') {
                    const priorities = {'critical': 4, 'high': 3, 'normal': 2, 'low': 1};
                    return (priorities[bVal] || 0) - (priorities[aVal] || 0);
                }
                return aVal.localeCompare(bVal);
            });
            
            container.innerHTML = '';
            items.forEach(item => container.appendChild(item));
        }
    </script>

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