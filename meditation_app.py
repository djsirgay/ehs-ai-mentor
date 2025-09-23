from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def meditation_app():
    return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Медитация</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
        }
        
        h1 {
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 300;
        }
        
        .timer {
            font-size: 4em;
            font-weight: 200;
            margin: 30px 0;
            font-family: 'Courier New', monospace;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin: 30px 0;
        }
        
        button {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .time-presets {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .preset-btn {
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 16px;
            font-size: 14px;
        }
        
        .sounds {
            margin-top: 30px;
        }
        
        .sound-btn {
            background: rgba(255, 255, 255, 0.1);
            margin: 5px;
            padding: 8px 16px;
            font-size: 14px;
        }
        
        .sound-btn.active {
            background: rgba(255, 255, 255, 0.3);
        }
        
        .breathing-guide {
            margin: 20px 0;
            font-size: 1.2em;
            opacity: 0;
            transition: opacity 0.5s ease;
        }
        
        .breathing-guide.active {
            opacity: 1;
        }
        
        .circle {
            width: 100px;
            height: 100px;
            border: 2px solid rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            margin: 20px auto;
            transition: transform 4s ease-in-out;
        }
        
        .circle.inhale {
            transform: scale(1.5);
        }
        
        .circle.exhale {
            transform: scale(1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧘‍♀️ Медитация</h1>
        
        <div class="timer" id="timer">05:00</div>
        
        <div class="time-presets">
            <button class="preset-btn" onclick="setTime(300)">5 мин</button>
            <button class="preset-btn" onclick="setTime(600)">10 мин</button>
            <button class="preset-btn" onclick="setTime(900)">15 мин</button>
            <button class="preset-btn" onclick="setTime(1200)">20 мин</button>
        </div>
        
        <div class="controls">
            <button onclick="startTimer()">▶️ Старт</button>
            <button onclick="pauseTimer()">⏸️ Пауза</button>
            <button onclick="resetTimer()">🔄 Сброс</button>
        </div>
        
        <div class="circle" id="breathingCircle"></div>
        
        <div class="breathing-guide" id="breathingGuide">
            Вдох...
        </div>
        
        <div class="sounds">
            <div style="margin-bottom: 15px;">Звуки природы:</div>
            <button class="sound-btn" onclick="toggleSound('rain')">🌧️ Дождь</button>
            <button class="sound-btn" onclick="toggleSound('ocean')">🌊 Океан</button>
            <button class="sound-btn" onclick="toggleSound('forest')">🌲 Лес</button>
            <button class="sound-btn" onclick="toggleSound('silence')">🔇 Тишина</button>
        </div>
    </div>

    <script>
        let timeLeft = 300; // 5 минут по умолчанию
        let timerInterval = null;
        let isRunning = false;
        let breathingInterval = null;
        let currentSound = null;
        
        // Звуки (используем Web Audio API для генерации)
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        let currentOscillator = null;
        
        function updateDisplay() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            document.getElementById('timer').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        function setTime(seconds) {
            if (!isRunning) {
                timeLeft = seconds;
                updateDisplay();
            }
        }
        
        function startTimer() {
            if (!isRunning && timeLeft > 0) {
                isRunning = true;
                startBreathingGuide();
                
                timerInterval = setInterval(() => {
                    timeLeft--;
                    updateDisplay();
                    
                    if (timeLeft <= 0) {
                        pauseTimer();
                        alert('🎉 Медитация завершена!');
                    }
                }, 1000);
            }
        }
        
        function pauseTimer() {
            isRunning = false;
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
            stopBreathingGuide();
        }
        
        function resetTimer() {
            pauseTimer();
            timeLeft = 300;
            updateDisplay();
        }
        
        function startBreathingGuide() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            guide.classList.add('active');
            
            let isInhaling = true;
            
            breathingInterval = setInterval(() => {
                if (isInhaling) {
                    guide.textContent = 'Вдох...';
                    circle.classList.remove('exhale');
                    circle.classList.add('inhale');
                } else {
                    guide.textContent = 'Выдох...';
                    circle.classList.remove('inhale');
                    circle.classList.add('exhale');
                }
                isInhaling = !isInhaling;
            }, 4000);
        }
        
        function stopBreathingGuide() {
            const guide = document.getElementById('breathingGuide');
            const circle = document.getElementById('breathingCircle');
            guide.classList.remove('active');
            circle.classList.remove('inhale', 'exhale');
            
            if (breathingInterval) {
                clearInterval(breathingInterval);
                breathingInterval = null;
            }
        }
        
        function toggleSound(soundType) {
            // Убираем активный класс со всех кнопок
            document.querySelectorAll('.sound-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Останавливаем текущий звук
            if (currentOscillator) {
                currentOscillator.stop();
                currentOscillator = null;
            }
            
            if (currentSound === soundType) {
                currentSound = null;
                return;
            }
            
            // Активируем выбранную кнопку
            event.target.classList.add('active');
            currentSound = soundType;
            
            // Запускаем новый звук
            if (soundType !== 'silence') {
                playNatureSound(soundType);
            }
        }
        
        function playNatureSound(type) {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Настройки для разных звуков
            switch(type) {
                case 'rain':
                    oscillator.type = 'white';
                    oscillator.frequency.setValueAtTime(200, audioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
                    break;
                case 'ocean':
                    oscillator.type = 'sine';
                    oscillator.frequency.setValueAtTime(80, audioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.15, audioContext.currentTime);
                    break;
                case 'forest':
                    oscillator.type = 'triangle';
                    oscillator.frequency.setValueAtTime(150, audioContext.currentTime);
                    gainNode.gain.setValueAtTime(0.08, audioContext.currentTime);
                    break;
            }
            
            oscillator.start();
            currentOscillator = oscillator;
        }
        
        // Инициализация
        updateDisplay();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)