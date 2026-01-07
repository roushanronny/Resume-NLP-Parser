# ⚡ Quick Deploy Guide (Hindi)

## 🎯 सबसे आसान तरीका: Streamlit Cloud

### Step 1: GitHub पर Code ✅ (Already Done!)
- Repository: https://github.com/roushanronny/Resume-NLP-Parser
- Code already push हो चुका है!

### Step 2: Streamlit Cloud पर Deploy करें

1. **Website खोलें:**
   ```
   https://streamlit.io/cloud
   ```

2. **Sign in करें:**
   - "Sign in" button click करें
   - GitHub account से login करें
   - Authorize Streamlit Cloud

3. **App Deploy करें:**
   - "New app" button click करें
   - **Repository:** `roushanronny/Resume-NLP-Parser` select करें
   - **Branch:** `main`
   - **Main file path:** `main.py`
   - **App URL:** (optional) custom name दे सकते हैं
   - **"Deploy!" button click करें**

4. **Wait करें:**
   - 5-10 minutes में app deploy हो जाएगी
   - आपको एक URL मिलेगा
   - Example: `https://resume-nlp-parser.streamlit.app`

5. **Done! 🎉**
   - App अब live है!
   - URL share करके किसी को भी access करा सकते हैं

---

## 📱 App Access:

Deploy होने के बाद:
- **Public URL:** `https://your-app-name.streamlit.app`
- **Share करें:** यह URL किसी को भी share कर सकते हैं
- **Update करें:** GitHub पर code push करने से automatically update होगा

---

## 🔄 Updates कैसे करें:

1. Local में changes करें
2. Git commit करें:
   ```bash
   git add .
   git commit -m "Updated features"
   git push origin main
   ```
3. Streamlit Cloud automatically detect करेगा और redeploy करेगा!

---

## 💡 Tips:

- ✅ **Free:** Streamlit Cloud completely free है
- ✅ **HTTPS:** Automatic SSL certificate
- ✅ **Auto-updates:** GitHub push = Auto deploy
- ✅ **No server management:** Everything handled automatically
- ✅ **Custom domain:** (Optional) अपना domain add कर सकते हैं

---

## 🆘 Troubleshooting:

**Problem:** Deploy नहीं हो रहा
- Check करें: Repository public है या Streamlit Cloud को access दिया है
- Check करें: `main.py` file root directory में है

**Problem:** Model download नहीं हो रहा
- `requirements.txt` में model URL already add है
- Automatically download होगा

**Problem:** Database error
- SQLite file local है, production में PostgreSQL use करें (optional)

---

**Ready to Deploy?** 👉 https://streamlit.io/cloud पर जाएं!

