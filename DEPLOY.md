# 🚀 Deployment Instructions

## GitHub Repository Setup

### 1. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `ehs-ai-mentor`
3. Description: `🛡️ EHS AI Mentor - Cal Poly Safety Platform with AI Training & Random Coffee`
4. Set to Public
5. Click "Create repository"

### 2. Push to GitHub
```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ehs-ai-mentor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Local Development

### Quick Start
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ehs-ai-mentor.git
cd ehs-ai-mentor

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_db.py

# Run application
python main_simple.py
```

### Access Application
- **Local URL:** http://localhost:8000
- **Dashboard:** http://localhost:8000/dashboard/u001

## Production Deployment

### Heroku Deployment
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn main_simple:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy to Heroku
heroku create ehs-ai-mentor
git push heroku main
```

### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy to Railway
railway login
railway init
railway up
```

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Create vercel.json
echo '{
  "builds": [
    {
      "src": "main_simple.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main_simple.py"
    }
  ]
}' > vercel.json

# Deploy
vercel
```

## Environment Variables

### Required Variables
```bash
# For production deployment
DATABASE_URL=sqlite:///./ehs_mentor.db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
```

## Features Checklist

- ✅ AI Safety Training System
- ✅ Random Coffee AI Matching
- ✅ Safety Store & Merch Integration
- ✅ Wellness & Meditation Features
- ✅ Gamification System
- ✅ Mobile-Responsive Design
- ✅ Dark Theme Support
- ✅ Real-time Chat System
- ✅ Badge & Achievement System
- ✅ Personalized Recommendations

## Tech Stack

- **Backend:** FastAPI, Python 3.8+
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (development), PostgreSQL (production)
- **Deployment:** Heroku, Railway, Vercel compatible
- **Features:** AI Matching, Real-time Chat, E-commerce

## Support

For issues and questions:
1. Check the README.md
2. Review the code documentation
3. Create GitHub Issues
4. Contact the development team

---

**🎓 Made with ❤️ for Cal Poly Students**