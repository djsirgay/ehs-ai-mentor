from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
import asyncio
import json
from ai_mentor import AIMentor
from pdf_processor import extract_text_from_pdf

app = FastAPI(title="EHS AI Mentor", version="1.0.0")
mentor = AIMentor()

async def process_users_stream(protocol_text: str):
    all_users = mentor.db.get_all_users()
    courses = mentor.db.get_all_courses()
    
    yield f"data: {json.dumps({'type': 'start', 'total': len(all_users)})}\n\n"
    
    assignments = []
    for i, user in enumerate(all_users):
        user_id = user['user_id']
        completed_courses = mentor.db.get_user_courses(user_id)
        user_data = dict(user)
        user_data['completed_courses'] = completed_courses
        
        # Отправляем прогресс
        yield f"data: {json.dumps({'type': 'progress', 'current': i+1, 'total': len(all_users), 'user': user['name']})}\n\n"
        
        decision = mentor.bedrock.analyze_protocol(protocol_text, user_data, courses)
        
        assignments_made = []
        if decision.get("should_assign") and decision.get("recommended_courses"):
            for course_id in decision["recommended_courses"]:
                existing = mentor.db.get_assignment_history(user_id, course_id)
                if not existing:
                    mentor.db.assign_course(user_id, course_id)
                    assignments_made.append(course_id)
        
        if assignments_made:
            assignment = {
                "user_id": user_id,
                "name": user['name'],
                "role": user['role'],
                "department": user['department'],
                "courses_assigned": assignments_made,
                "reason": decision.get("reason", "")
            }
            assignments.append(assignment)
            # Отправляем новое назначение
            yield f"data: {json.dumps({'type': 'assignment', 'assignment': assignment})}\n\n"
    
    yield f"data: {json.dumps({'type': 'complete', 'total_assignments': len(assignments)})}\n\n"

@app.post("/upload-pdf-stream")
async def upload_pdf_stream(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Только PDF файлы")
    
    pdf_bytes = await file.read()
    protocol_text = extract_text_from_pdf(pdf_bytes)
    
    return StreamingResponse(
        process_users_stream(protocol_text),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/")
async def root():
    html = '''
<!DOCTYPE html>
<html>
<head>
    <title>EHS AI Mentor - Real Time</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 30px; border-radius: 10px; }
        h1 { color: #333; text-align: center; font-weight: 400; }
        button { background: #007bff; color: white; cursor: pointer; font-size: 16px; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; border-left: 4px solid #28a745; }
        .progress { background: #e9ecef; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-bar { background: #007bff; height: 20px; transition: width 0.3s; }
        .assignment { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #007bff; }
        .course { background: #e7f3ff; padding: 4px 8px; margin: 2px; border-radius: 3px; display: inline-block; }
        #log { max-height: 400px; overflow-y: auto; background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>👋 EHS AI Mentor - Real Time</h1>
        <p><strong>Система в реальном времени показывает обработку каждого user</strong></p>
        
        <div style="margin: 20px 0; padding: 20px; background: #fff; border-radius: 5px; border: 2px dashed #ddd;">
            <label><strong>Загрузите PDF файл с протоколом:</strong></label><br>
            <input type="file" id="pdfFile" accept=".pdf" style="margin: 10px 0; padding: 10px;">
            <button onclick="uploadPDF()">📄 Анализировать в реальном времени</button>
        </div>

        <div id="result"></div>
        <div id="assignments"></div>
        <div id="log"></div>
    </div>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById('pdfFile');
            const resultDiv = document.getElementById('result');
            const assignmentsDiv = document.getElementById('assignments');
            const logDiv = document.getElementById('log');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<div class="result">Выберите PDF файл!</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result"><h3>🚀 Начинаю обработку...</h3></div>';
            assignmentsDiv.innerHTML = '';
            logDiv.innerHTML = '';

            try {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                const response = await fetch('/upload-pdf-stream', {
                    method: 'POST',
                    body: formData
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let assignments = [];

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\\n');
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'start') {
                                resultDiv.innerHTML = `
                                    <div class="result">
                                        <h3>📊 Обрабатываю ${data.total} пользователей</h3>
                                        <div class="progress">
                                            <div class="progress-bar" id="progressBar" style="width: 0%;"></div>
                                        </div>
                                        <p id="progressText">Готов к обработке...</p>
                                    </div>
                                `;
                            }
                            
                            if (data.type === 'progress') {
                                const percentage = Math.round((data.current / data.total) * 100);
                                document.getElementById('progressBar').style.width = percentage + '%';
                                document.getElementById('progressText').textContent = 
                                    `Обрабатываю: ${data.user} (${data.current}/${data.total}) - ${percentage}%`;
                                
                                logDiv.innerHTML += `<div>${new Date().toLocaleTimeString()}: Обрабатываю ${data.user}</div>`;
                                logDiv.scrollTop = logDiv.scrollHeight;
                            }
                            
                            if (data.type === 'assignment') {
                                assignments.push(data.assignment);
                                const assignment = data.assignment;
                                
                                assignmentsDiv.innerHTML += `
                                    <div class="assignment">
                                        <strong>${assignment.name}</strong> (${assignment.user_id}) - ${assignment.role}, ${assignment.department}<br>
                                        <strong>Курсы:</strong> ${assignment.courses_assigned.map(c => '<span class="course">📚 ' + c + '</span>').join(' ')}
                                        ${assignment.reason ? '<br><em>' + assignment.reason + '</em>' : ''}
                                    </div>
                                `;
                                
                                logDiv.innerHTML += `<div style="color: green;">${new Date().toLocaleTimeString()}: ✅ Назначены курсы для ${assignment.name}</div>`;
                                logDiv.scrollTop = logDiv.scrollHeight;
                            }
                            
                            if (data.type === 'complete') {
                                resultDiv.innerHTML += `<h3>✅ Завершено! Назначений: ${data.total_assignments}</h3>`;
                                logDiv.innerHTML += `<div style="color: blue; font-weight: bold;">${new Date().toLocaleTimeString()}: 🎉 Обработка завершена!</div>`;
                            }
                        }
                    }
                }

            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Error loading PDF</div>';
            }
        }
    </script>
</body>
</html>
    '''
    return HTMLResponse(content=html)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)