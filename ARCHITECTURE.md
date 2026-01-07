# 🏗️ Project Architecture - Resume NLP Parser

## 📋 Frontend और Backend क्या है?

### **Frontend (User Interface):**
Frontend वो part है जो user देखता है और interact करता है।

**इस Project में Frontend:**
- ✅ **Streamlit Framework** - यह frontend और backend दोनों handle करता है
- ✅ **HTML/CSS** - Custom styling और animations
- ✅ **User Interface Components:**
  - Navigation sidebar
  - File upload buttons
  - Cards और forms
  - Progress bars
  - Skill badges
  - Data display sections

**Frontend Files:**
- `main.py` - Main UI और navigation
- `modules/users.py` - User interface
- `modules/recruiters.py` - Recruiter interface
- `modules/admin.py` - Admin interface
- `modules/feedback.py` - Feedback interface
- CSS styling (main.py में embedded)

---

### **Backend (Logic और Processing):**
Backend वो part है जो data process करता है, calculations करता है, और database manage करता है।

**इस Project में Backend:**
- ✅ **Python Logic** - Resume parsing, NLP processing
- ✅ **NLP Processing:**
  - spaCy models (NER - Named Entity Recognition)
  - NLTK (Natural Language Toolkit)
  - Custom trained models
- ✅ **Database:**
  - SQLite database (`data/user_pdfs.db`)
  - CSV files for data storage
- ✅ **File Processing:**
  - PDF parsing (PyMuPDF)
  - Text extraction
  - Data analysis

**Backend Files:**
- `resume_parser.py` - Main parsing logic
- `modules/users.py` - User data processing
- `modules/admin.py` - Admin operations
- `modules/recruiters.py` - Recruiter search logic
- Database operations (SQLite)

---

## 🔄 How It Works (Architecture Flow):

```
User Uploads Resume (PDF)
         ↓
Frontend (Streamlit UI) receives file
         ↓
Backend (resume_parser.py) processes:
  - Extract text from PDF
  - Use spaCy for NLP
  - Extract name, email, skills, etc.
  - Calculate resume score
         ↓
Store in Database (SQLite)
         ↓
Display Results in Frontend (Streamlit UI)
```

---

## 🚀 Deployment Options:

### **Option 1: Streamlit Cloud (Recommended - FREE)**

**क्यों Best है:**
- ✅ Completely FREE
- ✅ No server setup needed
- ✅ Automatic deployment
- ✅ HTTPS included
- ✅ Easy updates (just push to GitHub)

**Steps:**
1. Code already GitHub पर है: https://github.com/roushanronny/Resume-NLP-Parser
2. https://streamlit.io/cloud पर जाएं
3. GitHub से sign in करें
4. "New app" click करें
5. Repository select करें: `roushanronny/Resume-NLP-Parser`
6. Main file: `main.py`
7. "Deploy!" click करें
8. 5-10 minutes में app live हो जाएगी!

**Result:** आपको मिलेगा: `https://resume-nlp-parser.streamlit.app`

---

### **Option 2: Heroku**

**Setup:**
```bash
# Heroku CLI install
brew install heroku

# Login
heroku login

# Create app
heroku create resume-nlp-parser

# Deploy
git push heroku main
```

**Note:** Heroku free tier अब available नहीं है, paid plan लेना होगा।

---

### **Option 3: AWS/Azure/GCP**

**AWS:**
- Elastic Beanstalk
- EC2 instance
- Lambda functions

**Azure:**
- App Service
- Container Instances

**Google Cloud:**
- Cloud Run
- App Engine

**Note:** ये options paid हैं और complex setup require करते हैं।

---

### **Option 4: VPS (Virtual Private Server)**

**Options:**
- DigitalOcean
- Linode
- Vultr
- AWS EC2

**Setup:**
1. Server rent करें
2. Python और dependencies install करें
3. App run करें
4. Nginx setup करें (reverse proxy)

---

## 📊 Current Architecture:

```
┌─────────────────────────────────────────┐
│         FRONTEND (Streamlit)            │
│  - User Interface                       │
│  - Forms, Buttons, Cards                │
│  - Data Display                         │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│         BACKEND (Python)                │
│  - resume_parser.py (NLP Processing)    │
│  - modules/*.py (Business Logic)       │
│  - PDF Processing                       │
│  - Data Extraction                      │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│         DATABASE (SQLite)               │
│  - user_pdfs.db (Resume Storage)       │
│  - CSV files (Skills, Positions)       │
└─────────────────────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│         ML MODELS                        │
│  - spaCy (en_core_web_sm)               │
│  - Custom NER Models (TrainedModel/)    │
└─────────────────────────────────────────┘
```

---

## 🎯 Deployment के लिए Important Points:

### **1. Streamlit Cloud (Best for this project):**
- ✅ Streamlit apps के लिए perfect
- ✅ Frontend + Backend automatically handle होता है
- ✅ No separate frontend/backend setup needed
- ✅ Free और easy

### **2. Traditional Deployment (अगर separate frontend/backend चाहिए):**
- Frontend: React/Vue/Angular (separate)
- Backend: Flask/FastAPI (separate API)
- Database: PostgreSQL/MySQL
- More complex setup

### **3. Current Project:**
- **Type:** Full-stack application (Streamlit)
- **Frontend:** Streamlit UI (Python-based)
- **Backend:** Python logic (same codebase)
- **Database:** SQLite (file-based)
- **Deployment:** Streamlit Cloud (easiest)

---

## ✅ Recommended Deployment:

**Streamlit Cloud** - क्योंकि:
1. यह Streamlit app है
2. Frontend और Backend एक ही codebase में है
3. No separate setup needed
4. Free और reliable
5. Automatic HTTPS
6. Easy updates

---

## 📝 Quick Deploy Command:

```bash
# Code already GitHub पर है, बस Streamlit Cloud पर deploy करें:
# 1. https://streamlit.io/cloud पर जाएं
# 2. Sign in with GitHub
# 3. New app → Select repository
# 4. Deploy!
```

---

## 🔗 Useful Links:

- **Streamlit Cloud:** https://streamlit.io/cloud
- **GitHub Repo:** https://github.com/roushanronny/Resume-NLP-Parser
- **Streamlit Docs:** https://docs.streamlit.io/

---

**Summary:** यह एक **Streamlit-based full-stack application** है जहाँ frontend और backend एक ही Python codebase में हैं। Streamlit Cloud पर deploy करना सबसे आसान और best option है!

