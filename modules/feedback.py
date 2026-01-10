import streamlit as st
from datetime import datetime

def process_feedback_mode():
    # Modern header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 0.5rem;">💬 Feedback Section</h1>
        <p style="color: #2d3748; font-size: 1.2rem; font-weight: 500;">We value your opinion! Help us improve</p>
    </div>
    """, unsafe_allow_html=True)

    # Feedback Form with better styling
    st.markdown("### 📝 Share Your Thoughts")
    
    with st.form("feedback_form", clear_on_submit=True):
        user_name = st.text_input("👤 Your Name:", placeholder="Enter your name")
        feedback = st.text_area(
            "💭 Provide feedback on the resume parser:", 
            height=150,
            placeholder="Tell us what you think about the application, what features you'd like to see, or any issues you encountered..."
        )
        
        submitted = st.form_submit_button("🚀 Submit Feedback", use_container_width=True)
        
        if submitted:
            if user_name and feedback:
                add_feedback(user_name, feedback)
                st.success("✅ Thank you! Your feedback has been submitted successfully!")
                st.balloons()
            else:
                st.warning("⚠️ Please fill in all fields before submitting.")
    
    # Additional info
    st.markdown("---")
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #667eea;">💡 What kind of feedback are we looking for?</h4>
        <ul style="color: #2d3748; margin: 1rem 0; padding-left: 2rem;">
            <li style="color: #2d3748; font-size: 1rem; line-height: 1.8; margin: 0.5rem 0; font-weight: 500;">✨ Feature suggestions</li>
            <li style="color: #2d3748; font-size: 1rem; line-height: 1.8; margin: 0.5rem 0; font-weight: 500;">🐛 Bug reports</li>
            <li style="color: #2d3748; font-size: 1rem; line-height: 1.8; margin: 0.5rem 0; font-weight: 500;">💡 Ideas for improvement</li>
            <li style="color: #2d3748; font-size: 1rem; line-height: 1.8; margin: 0.5rem 0; font-weight: 500;">⭐ General comments</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def add_feedback(user_name, feedback):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('data/feedback_data.csv', 'a') as file:
        file.write(f"User Name: {user_name}\n")
        file.write(f"Feedback: {feedback}\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write("-" * 50 + "\n")
