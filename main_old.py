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

class ProtocolAnalysis(BaseModel):
    protocol_text: str
    user_id: str

@app.post("/analyze-protocol")
async def analyze_protocol(request: ProtocolAnalysis):
    try:
        result = mentor.analyze_and_assign(request.protocol_text, request.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Только PDF файлы")
        
        # Читаем PDF файл
        pdf_bytes = await file.read()
        protocol_text = extract_text_from_pdf(pdf_bytes)
        
        # Анализируем для всех пользователей
        result = mentor.analyze_for_all_users(protocol_text)
        result["extracted_text"] = protocol_text[:500] + "..." if len(protocol_text) > 500 else protocol_text
        
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
        textarea { width: 100%; height: 200px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        select, button, input[type="file"] { padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #007bff; color: white; cursor: pointer; font-size: 16px; }
        .result { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; border-left: 4px solid #28a745; }
        .course { background: #e7f3ff; padding: 8px; margin: 5px 0; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ EHS AI Mentor</h1>
        <p><strong>Умная система для автоматического assignment курсов по охране труда</strong></p>
        


        <div>
            <label><strong>Введите новый протокол безопасности:</strong></label>
            <textarea id="protocol" placeholder="НОВЫЙ ПРОТОКОЛ БЕЗОПАСНОСТИ - Работа с химическими веществами\n\nВсе сотрудники должны знать основы обращения с опасными веществами..."></textarea>
        </div>

        <div style="margin: 20px 0; padding: 20px; background: #fff; border-radius: 5px; border: 2px dashed #ddd;">
            <label><strong>Загрузите PDF файл с протоколом:</strong></label><br>
            <p>Система автоматически проанализирует всех пользователей и назначит курсы тем, кому нужно</p>
            <input type="file" id="pdfFile" accept=".pdf" style="margin: 10px 0;">
            <button onclick="uploadPDF()">📄 Анализировать для всех</button>
        </div>

        <button onclick="analyzeProtocol()">🤖 Анализировать протокол</button>
        <div id="result"></div>
    </div>

    <script>
        async function analyzeProtocol() {
            const userId = document.getElementById('userId').value;
            const protocol = document.getElementById('protocol').value;
            const resultDiv = document.getElementById('result');

            if (!protocol.trim()) {
                resultDiv.innerHTML = '<div class="result">Введите текст протокола!</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">⏳ Анализирую протокол...</div>';

            try {
                const response = await fetch('/analyze-protocol', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        protocol_text: protocol,
                        user_id: userId
                    })
                });

                const data = await response.json();
                displayResult(data);

            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Error анализа</div>';
            }
        }

        async function uploadPDF() {
            const userId = document.getElementById('userId').value;
            const fileInput = document.getElementById('pdfFile');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<div class="result">Выберите PDF файл!</div>';
                return;
            }

            resultDiv.innerHTML = '<div class="result">⏳ Обрабатываю PDF...</div>';

            try {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                
                const response = await fetch(`/upload-pdf?user_id=${userId}`, {
                    method: 'POST',
                    body: formData
                });



                const data = await response.json();
                displayResult(data, true);

            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = '<div class="result">❌ Error loading PDF</div>';
            }
        }

        function displayResult(data, fromPDF = false) {
            const resultDiv = document.getElementById('result');
            
            let html = '<div class="result">';
            html += `<h3>✅ Анализ завершен для ${data.user_id}</h3>`;
            
            if (fromPDF && data.extracted_text) {
                html += `<p><strong>Извлеченный текст:</strong> ${data.extracted_text}</p>`;
            }
            
            html += `<p><strong>Решение AI:</strong> ${data.analysis.should_assign ? 'Назначить курсы' : 'Курсы не требуются'}</p>`;
            html += `<p><strong>Обоснование:</strong> ${data.analysis.reason}</p>`;
            
            if (data.assignments_made.length > 0) {
                html += '<h4>🎯 Назначенные курсы:</h4>';
                data.assignments_made.forEach(courseId => {
                    html += `<div class="course">📚 ${courseId}</div>`;
                });
            } else {
                html += '<p>Новые курсы не назначены</p>';
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