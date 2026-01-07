import streamlit as st
import spacy
from spacy.matcher import Matcher
import csv
import fitz  # PyMuPDF

# Load the SpaCy model
nlp = spacy.load('en_core_web_sm')

def process_recruiters_mode():
    # Modern header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 0.5rem;">💼 Recruiter's Panel</h1>
        <p style="color: #666; font-size: 1.2rem;">Find the perfect candidates for your job openings</p>
    </div>
    """, unsafe_allow_html=True)

    # File upload section
    st.markdown("### 📄 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload multiple PDF resumes", 
        accept_multiple_files=True,
        type="pdf",
        help="You can upload multiple resumes at once"
    )
    
    # Skills input section
    st.markdown("### 🎯 Required Skills")
    required_skills_input = st.text_input(
        "Enter required skills (comma-separated)", 
        "",
        placeholder="e.g., Python, Machine Learning, React, SQL"
    )
    required_skills = [skill.strip().lower() for skill in required_skills_input.split(',') if skill.strip()]
    
    # Save skills button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 Save Required Skills", use_container_width=True):
            if required_skills:
                save_required_skills(required_skills)
                st.success("✅ Skills saved successfully!")
            else:
                st.warning("⚠️ Please enter skills to save")

    # Process resumes
    all_skills_found = set()
    if uploaded_files:
        st.markdown(f"### 📊 Processing {len(uploaded_files)} Resume(s)")
        st.markdown("---")
        
        for idx, file in enumerate(uploaded_files, 1):
            with st.expander(f"📄 Resume {idx}: {file.name}", expanded=True):
                with st.spinner(f"Analyzing {file.name}..."):
                    text = extract_text_from_pdf(file)
                    doc = nlp(text)
                    candidate_name = extract_candidate_name(doc)
                    display_candidate_info(candidate_name, file.name)

                    parsed_skills = extract_all_skills(doc)
                    display_parsed_skills(parsed_skills)

                    if required_skills:
                        skills_found = extract_skills(doc, required_skills)
                        display_skills_found(required_skills, skills_found)
                        all_skills_found.update(skills_found)
        
        # Summary
        if required_skills:
            st.markdown("---")
            st.markdown("### 📈 Summary")
            match_percentage = (len(all_skills_found) / len(required_skills)) * 100 if required_skills else 0
            st.metric("Skills Match Rate", f"{match_percentage:.1f}%", f"{len(all_skills_found)}/{len(required_skills)} skills found")

def save_required_skills(required_skills):
    with open('data/UpdatedSkills.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        for skill in required_skills:
            writer.writerow([skill])

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract candidate's full name using SpaCy
def extract_candidate_name(doc):
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return "Candidate name not found"

# Function to extract all skills from the resume
def extract_all_skills(doc):
    all_skills = set()
    for token in doc:
        if token.pos_ == 'NOUN' and token.text.isalpha() and len(token.text) > 1:
            all_skills.add(token.text.lower())
    return all_skills

# Function to extract skills using SpaCy Matcher
def extract_skills(doc, required_skills):
    matcher = Matcher(nlp.vocab)
    skills_found = set()

    for skill in required_skills:
        pattern = [{"LOWER": skill}]
        matcher.add(skill, [pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        matched_skill = doc[start:end].text.lower()
        skills_found.add(matched_skill)

    return skills_found

# Function to parse all skills from UpdatedSkills.csv
def parse_all_skills():
    skills_list = set()
    with open('data/UpdatedSkills.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                skills_list.add(str(item).lower())
    
    return skills_list

# Function to display candidate information
def display_candidate_info(candidate_name, file_name):
    st.markdown(f"""
    <div class="info-card">
        <h4 style="color: #667eea;">👤 Candidate Information</h4>
        <p style="color: #333;"><strong>Name:</strong> {candidate_name}</p>
        <p style="color: #333;"><strong>File:</strong> {file_name}</p>
    </div>
    """, unsafe_allow_html=True)

# Function to display parsed skills from the resume
def display_parsed_skills(parsed_skills):
    if parsed_skills:
        skills_html = " ".join([f'<span class="skill-badge">{skill}</span>' for skill in list(parsed_skills)[:20]])
        st.markdown(f"""
        <div class="info-card">
            <h4 style="color: #667eea;">🛠️ Skills Found in Resume</h4>
            <div>{skills_html}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No skills parsed from resume")

# Function to display skills found or not
def display_skills_found(required_skills, skills_found):
    st.markdown("### ✅ Skills Match Analysis")
    
    found_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if skill in skills_found:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if found_skills:
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #10b981;">
                <h4 style="color: #10b981;">✅ Found ({len(found_skills)})</h4>
                <div>{" ".join([f'<span class="skill-badge" style="background: #10b981;">{skill}</span>' for skill in found_skills])}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if missing_skills:
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #ef4444;">
                <h4 style="color: #ef4444;">❌ Missing ({len(missing_skills)})</h4>
                <div>{" ".join([f'<span class="skill-badge" style="background: #ef4444;">{skill}</span>' for skill in missing_skills])}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    process_recruiters_mode()
