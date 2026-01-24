# 🚀 Quick Deployment Guide (Hindi)

## सबसे आसान तरीका: Streamlit Cloud (FREE)

### Step 1: GitHub पर Code Upload करें

```bash
# Terminal में project folder में जाएं
cd /Users/roushankumar/Desktop/Resume-NLP-Parser

# Git initialize करें
git init

# सभी files add करें
git add .

# Commit करें
git commit -m "Resume NLP Parser App"

# GitHub पर नया repository बनाएं (github.com पर)
# फिर नीचे commands run करें:
git remote add origin https://github.com/YOUR_USERNAME/Resume-NLP-Parser.git
git branch -M main
git push -u origin main
```

### Step 2: Streamlit Cloud पर Deploy करें

1. **Website खोलें:** https://streamlit.io/cloud
2. **Sign in करें:** GitHub account से login करें
3. **"New app" button click करें**
4. **Details भरें:**
   - Repository: अपना repository select करें
   - Branch: `main`
   - Main file path: `main.py`
5. **"Deploy!" button click करें**
6. **5-10 minutes wait करें** - App automatically deploy हो जाएगी!

### Step 3: App Access करें

- Deploy होने के बाद आपको एक URL मिलेगा
- Example: `https://your-app-name.streamlit.app`
- यह URL share करके किसी को भी access करा सकते हैं!

---

## Alternative: Heroku पर Deploy

### Step 1: Heroku Setup

```bash
# Heroku CLI install करें
brew install heroku

# Login करें
heroku login

# App create करें
heroku create resume-nlp-parser

# Deploy करें
git push heroku main
```

---

## Important Notes:

✅ **SpaCy Model:** Automatically download होगा  
✅ **Database:** SQLite local database है (production के लिए PostgreSQL use करें)  
✅ **Free Tier:** Streamlit Cloud free है unlimited apps के लिए  
✅ **Custom Domain:** Streamlit Cloud पर custom domain add कर सकते हैं  

---

## Troubleshooting:

**Problem:** Model download नहीं हो रहा  
**Solution:** `requirements.txt` में model URL already add है

**Problem:** App deploy नहीं हो रही  
**Solution:** 
- Check करें कि `main.py` file root directory में है
- `requirements.txt` सही है
- GitHub पर सभी files push हुई हैं

**Problem:** Database error  
**Solution:** SQLite file को `.gitignore` में add करें (already done)

---

## Support Links:

- 📚 Streamlit Docs: https://docs.streamlit.io/
- ☁️ Streamlit Cloud: https://streamlit.io/cloud
- 💬 Streamlit Community: https://discuss.streamlit.io/

---

**Happy Deploying! 🎉**


