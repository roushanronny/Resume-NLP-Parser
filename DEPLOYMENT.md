# 🚀 Deployment Guide - Resume NLP Parser

## Option 1: Streamlit Cloud (Recommended - FREE & EASY)

### Steps:

1. **GitHub पर Code Push करें:**
   ```bash
   # GitHub repository बनाएं
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/Resume-NLP-Parser.git
   git push -u origin main
   ```

2. **Streamlit Cloud पर Deploy:**
   - https://streamlit.io/cloud पर जाएं
   - "Sign up" करें (GitHub account से)
   - "New app" click करें
   - Repository select करें
   - Main file path: `main.py`
   - Branch: `main`
   - "Deploy!" button click करें

3. **App automatically deploy हो जाएगी!**

---

## Option 2: Heroku

### Steps:

1. **Heroku CLI Install करें:**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # या website से download करें: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Heroku Account बनाएं:**
   - https://www.heroku.com पर sign up करें

3. **Deploy करें:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **Requirements:**
   - `Procfile` file बनाएं (नीचे देखें)

---

## Option 3: AWS/Azure/GCP

### AWS Elastic Beanstalk:
- AWS account बनाएं
- Elastic Beanstalk service use करें
- Application upload करें

### Azure App Service:
- Azure account बनाएं
- App Service create करें
- Code deploy करें

### Google Cloud Run:
- GCP account बनाएं
- Cloud Run service use करें
- Container deploy करें

---

## Important Notes:

1. **SpaCy Model Download:**
   - Deployment पर spaCy model automatically download होगा
   - या `packages.txt` में add करें:
   ```
   https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
   ```

2. **Environment Variables:**
   - Secrets को `.streamlit/secrets.toml` में store करें
   - Production में secure credentials use करें

3. **Database:**
   - SQLite local database है
   - Production के लिए PostgreSQL या MySQL use करें

4. **File Size Limits:**
   - Streamlit Cloud: 1GB per app
   - Heroku: 500MB slug size

---

## Quick Deploy Commands:

```bash
# Git setup
git init
git add .
git commit -m "Ready for deployment"

# GitHub push
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main

# Streamlit Cloud पर जाकर deploy करें!
```

---

## Support:
- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Cloud: https://streamlit.io/cloud
- Heroku Docs: https://devcenter.heroku.com/


