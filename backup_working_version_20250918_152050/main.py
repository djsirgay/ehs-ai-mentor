from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os
from pydantic import BaseModel
from ai_mentor import AIMentor
from pdf_processor import extract_text_from_pdf

app = FastAPI(title="EHS AI Mentor", version="1.0.0")
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
mentor = AIMentor()

progress_data = {"current": 0, "total": 0}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Только PDF файлы")
        
        pdf_bytes = await file.read()
        protocol_text = extract_text_from_pdf(pdf_bytes)
        
        # Сбрасываем прогресс
        progress_data["current"] = 0
        progress_data["total"] = len(mentor.db.get_all_users())
        
        def update_progress(current, total):
            progress_data["current"] = current
            progress_data["total"] = total
        
        result = mentor.analyze_for_all_users(protocol_text, update_progress)
        result["extracted_text"] = protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/progress")
async def get_progress():
    return progress_data

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
        .course { background: #e7f3ff; padding: 8px; margin: 5px 0; border-radius: 3px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ EHS AI Mentor</h1>
        <p><strong>Умная система для автоматического назначения курсов по охране труда</strong></p>
        
        <div style="margin: 20px 0; padding: 20px; background: #fff; border-radius: 5px; border: 2px dashed #ddd;">
            <label><strong>Загрузите PDF файл с протоколом:</strong></label><br>
            <p>Система автоматически проанализирует всех пользователей и назначит курсы тем, кому нужно</p>
            <input type="file" id="pdfFile" accept=".pdf" style="margin: 10px 0; padding: 10px;">
            <button onclick="uploadPDF()">📄 Анализировать для всех</button>
        </div>

        <div id="result"></div>
    </div>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById('pdfFile');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<div class="result">Выберите PDF файл!</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result" id="statusDiv">⏳ Начинаю анализ...</div>';
            
            // Показываем что сервер работает
            let dots = 0;
            const statusInterval = setInterval(() => {
                dots = (dots + 1) % 4;
                const statusDiv = document.getElementById('statusDiv');
                if (statusDiv) {
                    statusDiv.innerHTML = '⏳ Анализирую 110 пользователей' + '.'.repeat(dots);
                }
            }, 500);

            try {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                const response = await fetch('/upload-pdf', {
                    method: 'POST',
                    body: formData
                });

                clearInterval(statusInterval);
                const data = await response.json();
                displayAllUsersResult(data);

            } catch (error) {
                clearInterval(statusInterval);
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Ошибка загрузки PDF</div>';
            }
        }

        function displayAllUsersResult(data) {
            const resultDiv = document.getElementById('result');
            
            let html = '<div class="result">';
            html += `<h3>✅ Анализ завершен для ${data.total_users} пользователей</h3>`;
            
            if (data.extracted_text) {
                html += `<p><strong>Протокол:</strong> ${data.extracted_text}</p>`;
            }
            
            if (data.assignments && data.assignments.length > 0) {
                html += `<h4>🎯 Назначения (${data.assignments.length} пользователей):</h4>`;
                
                data.assignments.forEach(assignment => {
                    html += `<div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff;">`;
                    html += `<strong>${assignment.name}</strong> (${assignment.user_id}) - ${assignment.role}, ${assignment.department}<br>`;
                    html += `<strong>Курсы:</strong> `;
                    assignment.courses_assigned.forEach(courseId => {
                        html += `<span class="course">📚 ${courseId}</span> `;
                    });
                    if (assignment.reason) {
                        html += `<br><em>${assignment.reason}</em>`;
                    }
                    html += `</div>`;
                });
            } else {
                html += '<p>Никому не нужны новые курсы по этому протоколу</p>';
            }
            
            html += '</div>';
            resultDiv.innerHTML = html;
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