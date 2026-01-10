# main.py
# Python 3.12+ compatibility patch for pydantic v1 (must be before any spacy imports)
import sys
if sys.version_info >= (3, 12):
    from typing import ForwardRef
    _original_evaluate = ForwardRef._evaluate
    
    def _patched_evaluate(self, globalns=None, localns=None, frozenset=None, type_params=None, **kwargs):
        # Handle Python 3.13+ signature with type_params
        # Remove type_params from kwargs if it was passed as positional
        if 'type_params' in kwargs and type_params is not None:
            # Both positional and keyword - remove from kwargs
            kwargs.pop('type_params', None)
        elif 'type_params' not in kwargs and type_params is None:
            # Neither provided - set default
            type_params = ()
        
        # Handle recursive_guard for older Python versions
        if 'recursive_guard' not in kwargs:
            kwargs['recursive_guard'] = set()
        
        # Call original with proper signature
        try:
            # Try Python 3.13+ signature first
            return _original_evaluate(self, globalns, localns, frozenset or set(), type_params=type_params, **kwargs)
        except TypeError:
            # Fallback for older signatures
            try:
                return _original_evaluate(self, globalns, localns, frozenset or set(), **kwargs)
            except TypeError:
                # Last resort - minimal call
                return _original_evaluate(self, globalns, localns, **kwargs)
    
    ForwardRef._evaluate = _patched_evaluate

import streamlit as st

# Import modules with error handling
try:
    from modules.users import process_user_mode
    from modules.recruiters import process_recruiters_mode
    from modules.admin import process_admin_mode
    from modules.feedback import process_feedback_mode
except Exception as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Custom CSS for modern UI
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Animated background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header styling with glassmorphism */
    .main-header {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        margin: 0;
        font-weight: 800;
        text-shadow: none;
        letter-spacing: -1px;
    }
    
    /* Card styling with glassmorphism and hover */
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
    }
    
    .info-card:hover::before {
        width: 100%;
        opacity: 0.1;
    }
    
    .info-card h3, .info-card h4 {
        color: #667eea;
        margin-top: 0;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    /* List items in info-card - ensure dark visible colors */
    .info-card ul, .info-card ol {
        color: #2d3748;
        margin: 1rem 0;
        padding-left: 2rem;
    }
    
    .info-card li {
        color: #2d3748;
        font-size: 1rem;
        line-height: 1.8;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* All text in info-card should be dark by default */
    .info-card, .info-card p, .info-card div, .info-card span {
        color: #2d3748;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Button styling with animation */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f4f8;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed #667eea;
        transition: all 0.3s;
    }
    
    .uploadedFile:hover {
        border-color: #764ba2;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f4f8;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* Skill badge with animation */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f4f8;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        margin: 0.4rem;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .skill-badge::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .skill-badge:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .skill-badge:hover {
        transform: translateY(-3px) scale(1.1);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Progress bar enhancement */
    .progress-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Section headers with gradient */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 4px solid;
        border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;
        position: relative;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 15px;
        padding: 1.5rem;
        color: #155724;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Resume Parser AI", 
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_custom_css()
    
    # Modern header with enhanced design
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Resume Parser AI</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem; font-weight: 300; color: #2d3748; text-shadow: 1px 1px 2px rgba(240,244,248,0.6);">
            Intelligent Resume Analysis with Advanced NLP Technology
        </p>
        <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
                <div style="font-size: 0.9rem; color: #2d3748; font-weight: 600;">Fast Processing</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <div style="font-size: 0.9rem; color: #2d3748; font-weight: 600;">Accurate Results</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
                <div style="font-size: 0.9rem; color: #2d3748; font-weight: 600;">Secure & Private</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced Sidebar
    st.sidebar.markdown("### 🎯 Navigation")
    st.sidebar.markdown("---")
    
    app_mode = st.sidebar.radio(
        "Choose a section:",
        ["👤 Users", "💼 Recruiters", "💬 Feedback", "⚙️ Admin"],
        label_visibility="visible"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-top: 2rem;">
        <h4 style="color: #667eea;">✨ Features</h4>
        <ul style="color: #2d3748; font-size: 0.9rem; margin: 0.5rem 0; padding-left: 1.5rem;">
            <li style="color: #2d3748; line-height: 1.6; margin: 0.3rem 0; font-weight: 500;">Smart Resume Parsing</li>
            <li style="color: #2d3748; line-height: 1.6; margin: 0.3rem 0; font-weight: 500;">Skill Extraction</li>
            <li style="color: #2d3748; line-height: 1.6; margin: 0.3rem 0; font-weight: 500;">Resume Scoring</li>
            <li style="color: #2d3748; line-height: 1.6; margin: 0.3rem 0; font-weight: 500;">Job Matching</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if "👤 Users" in app_mode:
        process_user_mode()
    elif "💼 Recruiters" in app_mode:
        process_recruiters_mode()
    elif "⚙️ Admin" in app_mode:
        process_admin_mode()
    elif "💬 Feedback" in app_mode:
        process_feedback_mode()

if __name__ == "__main__":
    main()




#  Streamlit, SpaCy, and PyMuPDF. //MVVI