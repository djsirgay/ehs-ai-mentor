# 🛡️ EHS AI Mentor - Cal Poly Safety Platform

**Умная AI-система для обучения по охране труда и социальных связей в Cal Poly**

## ✨ Основные возможности

### 🎯 **AI Safety Training**
- Автоматическое назначение курсов по охране труда
- Персонализированные рекомендации обучения
- Отслеживание прогресса и сертификации
- Система бейджей и достижений

### ☕ **Random Coffee AI**
- Умный алгоритм поиска друзей по интересам
- Анонимное сопоставление студентов
- AI-чат для знакомств и общения
- Персонализированные рекомендации встреч

### 🛒 **Safety Store & Merch**
- Магазин средств защиты и Cal Poly мерча
- Персонализированные рекомендации товаров
- Система скидок за прохождение курсов
- Интеграция с Amazon и Creator Spring

### 🧘 **Wellness Features**
- Медитация и дыхательные упражнения
- Мотивационные статусы
- Система релаксации
- Поддержка ментального здоровья

## 🚀 Быстрый запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных
```bash
python setup_db.py
```

### 3. Запуск приложения
```bash
python main_simple.py
```

### 4. Открыть в браузере
```
http://localhost:8000
```

## 📱 Адаптивный дизайн

- **Полностью адаптивный интерфейс** для всех устройств
- **Мобильная оптимизация** с touch-friendly элементами
- **Темная тема** для комфортного использования
- **Современный UI/UX** с градиентами и анимациями

## 🎨 Технологии

- **Backend:** FastAPI, Python
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite
- **AI:** Custom matching algorithms
- **Design:** Responsive, Mobile-first

## 📊 API Endpoints

### Safety Training
- `GET /dashboard/{user_id}` - Главная панель пользователя
- `POST /analyze-protocol` - Анализ протоколов безопасности
- `GET /courses/{user_id}` - Курсы пользователя
- `POST /complete-course` - Завершение курса

### Random Coffee
- `POST /enhanced-coffee/profile` - Создание профиля
- `GET /matches/{user_id}` - Получение совпадений
- `POST /chat/send` - Отправка сообщений

### Store & Merch
- `GET /store/products` - Товары магазина
- `POST /store/add-to-cart` - Добавление в корзину
- `GET /merch/feed/{user_id}` - Персонализированный мерч

## 🏗️ Архитектура

```
ehs-ai-mentor/
├── main_simple.py          # Основное приложение
├── user_dashboard.py       # Пользовательский интерфейс
├── setup_db.py            # Настройка базы данных
├── test_system.py         # Тесты системы
├── static/                # Статические файлы
│   ├── tahoe.css          # Основные стили
│   └── images/            # Изображения
└── requirements.txt       # Зависимости
```

## 🎯 Особенности

### AI Matching Algorithm
- Анализ интересов и совместимости
- Учет расписания и предпочтений
- Персонализированные рекомендации
- Анонимность до взаимного интереса

### Gamification
- Система бейджей за прохождение курсов
- Прогресс-бары и достижения
- Разблокировка эксклюзивного мерча
- Мотивационные элементы

### Mobile-First Design
- Адаптивная сетка для всех экранов
- Touch-friendly интерфейс
- Оптимизированная навигация
- Быстрая загрузка на мобильных

## 🔧 Разработка

### Локальная разработка
```bash
# Клонирование репозитория
git clone https://github.com/yourusername/ehs-ai-mentor.git
cd ehs-ai-mentor

# Установка зависимостей
pip install -r requirements.txt

# Запуск в режиме разработки
uvicorn main_simple:app --reload
```

### Тестирование
```bash
python test_system.py
```

## 📄 Лицензия

MIT License - см. файл LICENSE для деталей

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Контакты

- **Проект:** EHS AI Mentor
- **Университет:** Cal Poly
- **Цель:** Безопасность и социальные связи студентов

---

**🎓 Сделано с ❤️ для студентов Cal Poly**