import streamlit as st
import sqlite3

# Import with error handling
try:
    from resume_parser import extract_resume_info_from_pdf, extract_contact_number_from_resume, extract_education_from_resume, \
        extract_experience, suggest_skills_for_job, show_colored_skills, calculate_resume_score, extract_resume_info
except Exception as e:
    st.error(f"Error importing resume_parser: {e}")
    st.stop()

# Function to create a table for PDFs in SQLite database if it doesn't exist
def create_table():
    conn = sqlite3.connect('data/user_pdfs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_uploaded_pdfs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            data BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert PDF into the SQLite database
def insert_pdf(name, data):
    conn = sqlite3.connect('data/user_pdfs.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_uploaded_pdfs (name, data) VALUES (?, ?)', (name, data))
    conn.commit()
    conn.close()

def process_user_mode():
    create_table()  # Create table if it doesn't exist

    # Modern header with glassmorphism
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border-radius: 20px; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3rem; margin-bottom: 1rem; font-weight: 800;">👤 User Dashboard</h1>
        <p style="color: #333; font-size: 1.3rem; font-weight: 400;">Upload your resume and get instant AI-powered insights</p>
        <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            <span style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: #667eea; font-weight: 600;">📊 Analytics</span>
            <span style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: #667eea; font-weight: 600;">🎯 Scoring</span>
            <span style="background: rgba(102, 126, 234, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: #667eea; font-weight: 600;">💡 Recommendations</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Single file uploader with drag and drop functionality
    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume", 
        type="pdf",
        help="Drag and drop your PDF resume or click to browse. Limit 200MB per file.",
        label_visibility="visible"
    )

    if uploaded_file:
        # Success message
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")
        
        pdf_name = uploaded_file.name
        pdf_data = uploaded_file.getvalue()

        # Insert the uploaded PDF into the database
        insert_pdf(pdf_name, pdf_data)

        with st.spinner("🔄 Analyzing your resume... This may take a moment."):
            pdf_text = extract_resume_info_from_pdf(uploaded_file)
            resume_info = extract_resume_info(pdf_text)

        # Personal Information Section
        st.markdown('<div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = f"{resume_info['first_name']} {resume_info['last_name']}".strip()
            if not name or name == " ":
                name = "Not found"
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">👤</div>
                    <h4 style="color: #667eea; margin: 0; font-size: 1.1rem;">Name</h4>
                </div>
                <p style="font-size: 1.3rem; font-weight: 700; color: #333; margin: 0;">{name}</p>
            </div>
            """, unsafe_allow_html=True)
            
            email = resume_info['email'] if resume_info['email'] else "Not found"
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">📧</div>
                    <h4 style="color: #667eea; margin: 0; font-size: 1.1rem;">Email</h4>
                </div>
                <p style="font-size: 1.1rem; color: #333; margin: 0; word-break: break-word;">{email}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            contact_number = extract_contact_number_from_resume(pdf_text)
            if contact_number == "Not found":
                phone_display = "Not found"
            else:
                phone_display = f"+{contact_number}"
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">📱</div>
                    <h4 style="color: #667eea; margin: 0; font-size: 1.1rem;">Phone</h4>
                </div>
                <p style="font-size: 1.1rem; color: #333; margin: 0;">{phone_display}</p>
            </div>
            """, unsafe_allow_html=True)
            
            degree = resume_info['degree_major'] if resume_info['degree_major'] else "Not found"
            st.markdown(f"""
            <div class="info-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">🎓</div>
                    <h4 style="color: #667eea; margin: 0; font-size: 1.1rem;">Degree/Major</h4>
                </div>
                <p style="font-size: 1.1rem; color: #333; margin: 0;">{degree}</p>
            </div>
            """, unsafe_allow_html=True)

        # Education Section
        st.markdown('<div class="section-header">🎓 Education</div>', unsafe_allow_html=True)
        education_info = extract_education_from_resume(pdf_text)
        if education_info:
            st.markdown(f"""
            <div class="info-card">
                <p style="font-size: 1.1rem; line-height: 1.8; color: #333;">{', '.join(education_info)}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No education information found in the resume.")

        # Skills Section
        st.markdown('<div class="section-header">🛠️ Skills</div>', unsafe_allow_html=True)
        show_colored_skills(resume_info['skills'])

        # Experience Section
        st.markdown('<div class="section-header">💼 Experience</div>', unsafe_allow_html=True)
        experience_info = extract_experience(pdf_text)
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="color: #667eea;">📊 Experience Level</h4>
                <p style="font-size: 1.2rem; font-weight: 600; color: #667eea;">{experience_info['level_of_experience']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="color: #667eea;">🎯 Suggested Position</h4>
                <p style="font-size: 1.2rem; font-weight: 600; color: #764ba2;">{experience_info['suggested_position']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Resume Score Section
        st.markdown('<div class="section-header">📈 Resume Score</div>', unsafe_allow_html=True)
        resume_score = calculate_resume_score(resume_info)
        
        # Enhanced progress bar
        percentage = resume_score
        percentage_str = str(percentage)
        
        # Color based on score
        if percentage >= 80:
            color = "#10b981"  # Green
        elif percentage >= 60:
            color = "#f59e0b"  # Orange
        else:
            color = "#ef4444"  # Red
        
        st.markdown(f"""
        <div style="background: #f0f0f0; border-radius: 15px; padding: 1rem; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem; font-weight: 700; color: {color};">{percentage}%</span>
                <span style="color: #2d3748; font-weight: 500;">Out of 100</span>
            </div>
            <div style="background: linear-gradient(90deg, {color} {percentage_str}%, #e5e7eb {percentage_str}%); height: 35px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); position: relative;">
                <span style="color: #1a1a2e; font-weight: 700; font-size: 1.1rem; text-shadow: 0 1px 3px rgba(240,244,248,0.8);">{percentage}% Complete</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggested Skills Section
        st.markdown('<div class="section-header">💡 Job Skill Recommendations</div>', unsafe_allow_html=True)
        desired_job = st.text_input(
            "🎯 Enter the job you are looking for:",
            placeholder="e.g., Software Engineer, Data Scientist, Product Manager"
        )
        
        if desired_job:
            suggested_skills = suggest_skills_for_job(desired_job)
            if suggested_skills:
                # Format skills as badges
                skills_badges = " ".join([f'<span class="skill-badge">{skill}</span>' for skill in suggested_skills if skill])
                st.markdown(f"""
                <div class="info-card">
                    <h4 style="color: #667eea;">✨ Recommended Skills for {desired_job}</h4>
                    <div style="margin-top: 1rem;">{skills_badges}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"No specific skill recommendations found for '{desired_job}'. Try a different job title.")

if __name__ == '__main__':
    process_user_mode()
