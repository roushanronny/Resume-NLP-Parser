import base64
import sqlite3
import streamlit as st
import pandas as pd

def process_admin_mode():
    # Modern header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 0.5rem;">⚙️ Admin Panel</h1>
        <p style="color: #666; font-size: 1.2rem;">Manage resumes and feedback</p>
    </div>
    """, unsafe_allow_html=True)

    # Admin authentication with better styling
    st.markdown("### 🔐 Authentication Required")
    
    with st.form("admin_login"):
        username = st.text_input("👤 Username:", placeholder="Enter admin username")
        password = st.text_input("🔑 Password:", type="password", placeholder="Enter admin password")
        login_button = st.form_submit_button("🚀 Login", use_container_width=True)
        
        if login_button:
            if authenticate_admin(username, password):
                st.session_state['admin_authenticated'] = True
                st.success("✅ Authentication successful!")
                st.balloons()
            else:
                st.error("❌ Authentication failed. Please try again.")
                st.session_state['admin_authenticated'] = False
    
    # Display content if authenticated
    if st.session_state.get('admin_authenticated', False):
        st.markdown("---")
        
        # Display uploaded PDFs in a table with download links and name fields
        display_uploaded_pdfs()

        st.markdown('---')
        
        # Display feedback data
        display_feedback_data()
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['admin_authenticated'] = False
            st.rerun()

def authenticate_admin(username, password):
    # Updated credentials
    hardcoded_username = "roushanyadav"
    hardcoded_password = "12345"
    return username == hardcoded_username and password == hardcoded_password

def display_feedback_data():
    st.markdown("### 💬 Feedback Management")
    try:
        with open('data/feedback_data.csv', 'r') as file:
            feedback_content = file.read()
        
        if feedback_content.strip():
            # Parse and display feedbacks in a nicer format
            feedbacks = feedback_content.split('-' * 50)
            feedbacks = [f.strip() for f in feedbacks if f.strip()]
            
            st.markdown(f"**Total Feedbacks:** {len(feedbacks)}")
            
            # Display latest 5 feedbacks
            for idx, feedback in enumerate(feedbacks[-5:], 1):
                st.markdown(f"""
                <div class="info-card">
                    <h4 style="color: #667eea;">Feedback #{len(feedbacks) - 5 + idx}</h4>
                    <pre style="white-space: pre-wrap; font-family: inherit; color: #333;">{feedback}</pre>
                </div>
                """, unsafe_allow_html=True)
            
            if len(feedbacks) > 5:
                if st.button("📋 View All Feedbacks"):
                    for idx, feedback in enumerate(feedbacks, 1):
                        st.markdown(f"""
                        <div class="info-card">
                            <h4 style="color: #667eea;">Feedback #{idx}</h4>
                            <pre style="white-space: pre-wrap; font-family: inherit; color: #333;">{feedback}</pre>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📭 No feedback data available yet.")

    except FileNotFoundError:
        st.warning("⚠️ No feedback data file found.")

def get_uploaded_pdfs():
    try:
        conn = sqlite3.connect('data/user_pdfs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM user_uploaded_pdfs")
        uploaded_pdfs = cursor.fetchall()
        conn.close()
        return uploaded_pdfs

    except sqlite3.Error as e:
        st.error(f"Error fetching uploaded PDFs: {e}")
        return []

def display_uploaded_pdfs():
    uploaded_pdfs = get_uploaded_pdfs()

    if uploaded_pdfs:
        st.markdown("### 📄 Uploaded Resumes")
        st.markdown(f"**Total Resumes:** {len(uploaded_pdfs)}")
        
        # Display in a modern card format
        for pdf_id, pdf_name in uploaded_pdfs:
            pdf_data = get_pdf_data(pdf_id)
            if pdf_data:
                pdf_b64 = base64.b64encode(pdf_data[1]).decode('utf-8')
                download_link = f'<a href="data:application/pdf;base64,{pdf_b64}" download="{pdf_name}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 5px; text-decoration: none; font-weight: 600;">📥 Download</a>'
                
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #667eea;">📄 {pdf_name}</h4>
                            <p style="color: #666; margin: 0.5rem 0 0 0;">ID: {pdf_id}</p>
                        </div>
                        <div>{download_link}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ Error retrieving PDF data for ID: {pdf_id}")

    else:
        st.info("📭 No uploaded PDFs available yet.")

def get_pdf_data(pdf_id):
    try:
        conn = sqlite3.connect('data/user_pdfs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, data FROM user_uploaded_pdfs WHERE id=?", (pdf_id,))
        pdf_data = cursor.fetchone()
        conn.close()
        return pdf_data

    except sqlite3.Error as e:
        st.error(f"Error fetching PDF data: {e}")
        return None

if __name__ == "__main__":
    process_admin_mode()
