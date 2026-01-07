import re
import fitz
import base64
import streamlit as st
import spacy
import csv
import nltk

# Additional libraries
nltk.download('punkt')

# Load the spaCy model for English with error handling
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    # If model not found, download it
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

def load_keywords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            keywords = set()
            for row in reader:
                if row and row[0].strip():  # Check if row has data and first column is not empty
                    keyword = row[0].strip()
                    if keyword:  # Only add non-empty keywords
                        keywords.add(keyword)
            return keywords
    except Exception as e:
        st.warning(f"Error loading keywords from {file_path}: {e}")
        return set()

# ----------------------------------Extract Name----------------------------------
def extract_name(doc):
    # Get text from doc object
    if hasattr(doc, 'text'):
        text = doc.text
        processed_doc = doc
    else:
        text = str(doc)
        processed_doc = nlp(text)
    
    # Organization/institute keywords to exclude
    org_keywords = ['national', 'institute', 'technology', 'university', 'college', 'school', 
                   'academy', 'center', 'centre', 'foundation', 'corporation', 'company', 'ltd',
                   'limited', 'inc', 'llc', 'pvt', 'private']
    
    # Get entities
    entities = processed_doc.ents
    
    # Look for PERSON entities, prioritize those at the beginning of the document
    person_entities = []
    for ent in entities:
        if ent.label_ == 'PERSON':
            names = ent.text.split()
            ent_lower = ent.text.lower()
            
            # Filter out common false positives and organization names
            invalid_names = {'machine learning', 'deep learning', 'data science', 'artificial intelligence',
                           'software engineer', 'software developer', 'research consultant'}
            
            # Check if it contains organization keywords
            is_org = any(keyword in ent_lower for keyword in org_keywords)
            
            if ent_lower not in invalid_names and not is_org:
                # Check if it looks like a real name (2-4 words, all title case)
                if 2 <= len(names) <= 4 and all(name.istitle() and name.isalpha() for name in names):
                    person_entities.append(ent)
    
    # Return the first valid person entity (usually the candidate's name)
    if person_entities:
        names = person_entities[0].text.split()
        if len(names) >= 2:
            return names[0], ' '.join(names[1:])
        else:
            return person_entities[0].text, ""
    
    # Fallback: try to extract from first few lines (prioritize first line)
    lines = text.splitlines()[:15]  # Check first 15 lines
    
    # First, try the very first non-empty line (most likely to contain name)
    for idx, line in enumerate(lines[:3]):  # Prioritize first 3 lines
        line = line.strip()
        if not line:
            continue
        
        # Skip lines that are clearly not names
        if any(word in line.lower() for word in ['email', 'phone', 'address', 'resume', 'cv', 'objective', 'summary', 
                                                 'linkedin', 'github', 'portfolio', 'website']):
            continue
        
        # Skip if it contains organization keywords
        if any(keyword in line.lower() for keyword in org_keywords):
            continue
        
        words = line.split()
        # Look for 2-3 word patterns that look like names
        if 2 <= len(words) <= 3:
            potential_first = words[0]
            potential_last = ' '.join(words[1:])
            
            # Validation: should be title case, alphabetic, reasonable length
            if (potential_first.istitle() and potential_first.isalpha() and 
                len(potential_first) >= 2 and len(potential_first) <= 20 and
                all(w.replace(' ', '').isalpha() for w in words[1:]) and
                all(len(w) >= 2 and len(w) <= 20 for w in words[1:])):
                # Additional check: not common words or organization terms
                if (potential_first.lower() not in ['mr', 'mrs', 'ms', 'dr', 'prof', 'the', 'national', 'institute'] and
                    not any(org in potential_last.lower() for org in org_keywords)):
                    return potential_first, potential_last
    
    # Last resort: check first 2-3 words of first non-empty line (with strict validation)
    for line in lines[:5]:  # Only check first 5 lines
        line = line.strip()
        if not line:
            continue
        
        # Skip if contains organization keywords
        if any(keyword in line.lower() for keyword in org_keywords):
            continue
        
        words = line.split()[:3]
        if len(words) >= 2:
            first = words[0]
            last = ' '.join(words[1:])
            
            # Strict validation
            if (first.istitle() and first.isalpha() and 
                len(first) >= 2 and len(first) <= 15 and
                all(w.isalpha() for w in words[1:]) and
                all(len(w) >= 2 and len(w) <= 15 for w in words[1:]) and
                first.lower() not in ['national', 'institute', 'university', 'college', 'the', 'mr', 'mrs', 'ms', 'dr'] and
                not any(org in last.lower() for org in org_keywords)):
                return first, last
    
    return "", ""
# --------------------------------------------------------------------------------

# ----------------------------------Extract Email---------------------------------
def extract_email(doc):
    matcher = spacy.matcher.Matcher(nlp.vocab)
    email_pattern = [{'LIKE_EMAIL': True}]
    matcher.add('EMAIL', [email_pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        if match_id == nlp.vocab.strings['EMAIL']:
            return doc[start:end].text
    return ""
# --------------------------------------------------------------------------------

# ----------------------------------Extract Ph No---------------------------------
def extract_contact_number_from_resume(doc):
    contact_number = None
    # Handle both doc object and text string
    if hasattr(doc, 'text'):
        text = doc.text
    else:
        text = str(doc)
    
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()
    return contact_number if contact_number else "Not found"
# --------------------------------------------------------------------------------

# --------------------------------Extract Education-------------------------------
def extract_education_from_resume(doc):
    universities = []

    # Handle both doc object and text string
    if hasattr(doc, 'ents'):
        # Already a processed doc
        processed_doc = doc
    else:
        # It's text, need to process
        processed_doc = nlp(str(doc))

    # Iterate through entities and check for organizations (universities)
    for entity in processed_doc.ents:
        if entity.label_ == "ORG" and ("university" in entity.text.lower() or "college" in entity.text.lower() or "institute" in entity.text.lower()):
            universities.append(entity.text)

    return universities
# --------------------------------------------------------------------------------

# ----------------------------------Extract Skills--------------------------------
def csv_skills(doc):
    try:
        skills_keywords = load_keywords('data/newSkills.csv')
        skills = set()
        
        # Get text from doc object or use as string
        if hasattr(doc, 'text'):
            text = doc.text.lower()
        else:
            text = str(doc).lower()

        # Create a set of all words in the text for faster lookup
        words_in_text = set(re.findall(r'\b\w+\b', text))
        
        # Also check for multi-word skills
        text_lower = text.lower()
        
        for keyword in skills_keywords:
            if not keyword or not keyword.strip():
                continue
                
            keyword_lower = keyword.lower().strip()
            
            # Skip if keyword is too short or invalid
            if len(keyword_lower) < 2:
                continue
            
            # Match whole word only (not substring)
            # Check if keyword appears as a whole word in text
            pattern = r'\b' + re.escape(keyword_lower) + r'\b'
            if re.search(pattern, text_lower):
                # Additional validation
                if is_valid_skill(keyword):
                    skills.add(keyword)

        return skills
    except Exception as e:
        if 'st' in globals():
            st.warning(f"Error loading skills from CSV: {e}")
        return set()

# Load NER model with error handling
try:
    nlp_skills = spacy.load('TrainedModel/skills')
except Exception as e:
    nlp_skills = None
    st.warning(f"Could not load NER model: {e}. Using CSV skills only.")

def extract_skills_from_ner(doc):
    if nlp_skills is None:
        return set()
    
    non_skill_labels = {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'EMAIL'}
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
    
    skills = set()
    
    # Get text from doc object
    if hasattr(doc, 'text'):
        text = doc.text
    else:
        text = str(doc)
    
    try:
        for ent in nlp_skills(text).ents:
            if ent.label_ == 'SKILL':
                skill_text = ent.text.strip()
                skill_lower = skill_text.lower()
                
                # Filter out common words, numbers, and very short skills
                if (len(skill_text) >= 2 and 
                    skill_lower not in common_words and 
                    not skill_text.isdigit() and
                    not all(c.isdigit() for c in skill_text)):
                    # Keep original case for proper nouns, lowercase for others
                    if skill_text[0].isupper() and len(skill_text) > 3:
                        skills.add(skill_text)
                    else:
                        skills.add(skill_lower)
    except Exception as e:
        st.warning(f"Error in NER skill extraction: {e}")
    
    return skills

def is_valid_skill(skill_text):
    """Enhanced validation for skills - filters out non-skill items"""
    if not skill_text or len(skill_text) < 2:
        return False
    
    skill_text = skill_text.strip()
    skill_lower = skill_text.lower()
    
    # Common words to exclude
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 
        'as', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'admin', 'present', 'remote', 'built', 'conducted', 'optimized', 'resolved', 'stored', 'working',
        'other', 'skills', 'pre', 'jul', 'nov', 'sep', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'aug', 'oct', 'dec',
        'learning', 'certificate', 'consultant', 'inspection', 'labs'
    }
    
    # Phrases that are NOT skills (section headers, labels, etc.)
    non_skill_phrases = {
        'other skills', 'technical skills', 'core skills', 'key skills', 'professional skills',
        'linkedin learning', 'online learning', 'development certificate', 'research consultant',
        'acg inspection', 'data labs', 'l4 cloud', 'software developer', 'software engineer'
    }
    
    # Check if it's a non-skill phrase
    if skill_lower in non_skill_phrases:
        return False
    
    # Check if it contains non-skill words
    if any(phrase in skill_lower for phrase in ['other skills', 'technical skills', 'core skills', 'key skills']):
        return False
    
    # Exclude if it ends with common non-skill suffixes
    non_skill_suffixes = [' learning', ' certificate', ' consultant', ' inspection', ' labs', ' developer', ' engineer']
    if any(skill_lower.endswith(suffix) for suffix in non_skill_suffixes):
        return False
    
    # Exclude common words
    if skill_lower in common_words:
        return False
    
    # Exclude if it starts with common prefixes that indicate it's not a skill
    invalid_prefixes = ['•', ':', '(', ')', '@', '+', 'roushan', 'kumar', 'yadav', 'gmail', 'com']
    if any(skill_text.startswith(prefix) for prefix in invalid_prefixes):
        return False
    
    # Exclude if it starts or ends with dash (location/status indicators)
    if skill_text.startswith('-') or skill_text.endswith('-'):
        return False
    
    # Exclude if it's a location pattern (starts with dash and city name)
    if skill_text.startswith('-') and len(skill_text) > 1:
        return False
    
    # Exclude if it contains email pattern
    if '@' in skill_text or '.com' in skill_lower or '.in' in skill_lower:
        return False
    
    # Exclude phone numbers (contains digits with dashes or spaces)
    if re.search(r'\d{3,}', skill_text):  # 3 or more consecutive digits
        return False
    
    # Exclude if it's all digits
    if skill_text.replace('-', '').replace('.', '').isdigit():
        return False
    
    # Exclude dates (patterns like 2021-, 2023-, -2021, etc.)
    if re.search(r'\d{4}[-]?', skill_text) or re.search(r'[-]?\d{4}', skill_text):
        return False
    
    # Exclude month abbreviations with dots (Nov., Dec., etc.)
    if re.search(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\.?$', skill_lower):
        return False
    
    # Exclude if it contains location patterns (city names with dashes)
    city_patterns = ['bengaluru', 'hyderabad', 'mumbai', 'delhi', 'bangalore', 'pune']
    if any(city in skill_lower for city in city_patterns) and ('-' in skill_text or skill_text.startswith('-')):
        return False
    
    # Exclude locations (common location indicators) - including with dashes
    location_indicators = ['bengaluru', 'hyderabad', 'mumbai', 'delhi', 'bangalore', 'pune', 'chennai', 
                          'kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur', 'indore',
                          'thane', 'bhopal', 'visakhapatnam', 'patna', 'vadodara', 'ghaziabad',
                          '-bengaluru', '-hyderabad', '-mumbai', '-delhi', '-bangalore', '-pune']
    if skill_lower in location_indicators or any(loc in skill_lower for loc in ['-bengaluru', '-hyderabad', '-mumbai', '-delhi']):
        return False
    
    # Exclude status words
    status_words = ['present', 'remote', 'full-time', 'part-time', 'contract', 'internship', 
                    '-present', '-remote', '-full', '-part', 'current', '-current']
    if skill_lower in status_words or any(sw in skill_lower for sw in ['-present', '-remote']):
        return False
    
    # Exclude month abbreviations
    month_abbrevs = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                     'jan.', 'feb.', 'mar.', 'apr.', 'may.', 'jun.', 'jul.', 'aug.', 'sep.', 'oct.', 'nov.', 'dec.']
    if skill_lower in month_abbrevs or skill_lower.endswith('nov.') or skill_lower.startswith('nov.'):
        return False
    
    # Exclude organization/institute names
    org_keywords = ['national institute', 'institute of technology', 'university', 'college', 
                   'national institute of', 'institute']
    if any(org in skill_lower for org in org_keywords):
        return False
    
    # Exclude company names (common companies)
    company_names = ['microsoft', 'google', 'amazon', 'goldman', 'sachs', 'apple', 'meta', 'facebook',
                    'netflix', 'uber', 'airbnb', 'tesla', 'nvidia', 'oracle', 'ibm', 'adobe']
    if any(company in skill_lower for company in company_names):
        return False
    
    # Exclude if it's mostly special characters
    alnum_count = sum(1 for c in skill_text if c.isalnum())
    if alnum_count < len(skill_text) * 0.6:  # At least 60% should be alphanumeric
        return False
    
    # Exclude single character or very short non-meaningful words
    if len(skill_text) < 3 and skill_lower not in ['ai', 'ui', 'ux', 'os', 'db', 'ml', 'dl', 'nlp', 'api']:
        return False
    
    # Exclude if it contains only special characters and numbers
    if not any(c.isalpha() for c in skill_text):
        return False
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', skill_text):
        return False
    
    return True

def extract_skills(doc):
    # Get skills from CSV (more reliable)
    skills_csv = csv_skills(doc)
    
    # Get skills from NER (may have false positives)
    skills_ner = extract_skills_from_ner(doc)
    
    # Filter both sets with strict validation
    filtered_skills_csv = set()
    for skill in skills_csv:
        if is_valid_skill(skill):
            # Clean the skill text
            cleaned_skill = skill.strip()
            # Remove leading/trailing special characters
            cleaned_skill = re.sub(r'^[-•:()]+|[-•:()]+$', '', cleaned_skill)
            # Remove leading dashes (location/status indicators)
            cleaned_skill = cleaned_skill.lstrip('-')
            if cleaned_skill and is_valid_skill(cleaned_skill):
                filtered_skills_csv.add(cleaned_skill)
    
    filtered_skills_ner = set()
    for skill in skills_ner:
        if is_valid_skill(skill):
            # Clean the skill text
            cleaned_skill = skill.strip()
            # Remove leading/trailing special characters
            cleaned_skill = re.sub(r'^[-•:()]+|[-•:()]+$', '', cleaned_skill)
            # Remove leading dashes
            cleaned_skill = cleaned_skill.lstrip('-')
            if cleaned_skill and is_valid_skill(cleaned_skill):
                filtered_skills_ner.add(cleaned_skill)
    
    # Prioritize CSV skills, add NER skills that are not in CSV
    combined_skills = filtered_skills_csv.copy()
    
    # Only add NER skills that are not already in CSV and are meaningful
    for ner_skill in filtered_skills_ner:
        skill_lower = ner_skill.lower()
        # Check if this skill or similar is already in CSV
        if not any(skill_lower == csv_skill.lower() for csv_skill in filtered_skills_csv):
            # Additional validation
            if len(ner_skill) >= 3 and is_valid_skill(ner_skill):
                combined_skills.add(ner_skill)
    
    # Final cleanup - remove any remaining invalid items
    final_skills = []
    invalid_patterns = [
        r'^-',  # Starts with dash
        r'-$',  # Ends with dash
        r'\b(nov|dec|jan|feb|mar|apr|may|jun|jul|aug|sep|oct)\.?\b',  # Month abbreviations
        r'\b(bengaluru|hyderabad|mumbai|delhi|bangalore|pune)\b',  # City names
        r'\b(present|remote|full-time|part-time)\b',  # Status words
        r'\b(national institute|institute of technology|university|college)\b',  # Organizations
    ]
    
    # Non-skill phrases to exclude
    non_skill_phrases = {
        'other skills', 'technical skills', 'core skills', 'key skills', 'professional skills',
        'linkedin learning', 'online learning', 'development certificate', 'research consultant',
        'acg inspection', 'data labs', 'l4 cloud', 'software developer', 'software engineer',
        'feature engineering', 'model evaluation'
    }
    
    for skill in combined_skills:
        skill_lower = skill.lower().strip()
        
        # Skip if it's a known non-skill phrase
        if skill_lower in non_skill_phrases:
            continue
        
        # Skip if it contains non-skill keywords
        if any(phrase in skill_lower for phrase in ['other skills', 'technical skills', 'learning', 'certificate', 'consultant', 'inspection', 'labs']):
            # But allow if it's a valid technical term (like "machine learning")
            if skill_lower not in ['machine learning', 'deep learning', 'reinforcement learning']:
                continue
        
        # Check against invalid patterns
        is_invalid = False
        for pattern in invalid_patterns:
            if re.search(pattern, skill_lower):
                is_invalid = True
                break
        
        if not is_invalid and is_valid_skill(skill):
            final_skills.append(skill)
    
    # Sort and return as list (limit to top 30 most relevant)
    return sorted(list(set(final_skills)), key=str.lower)[:30]

# --------------------------------------------------------------------------------

# ----------------------------------Extract Major---------------------------------
def extract_major(doc):
    major_keywords = load_keywords('data/majors.csv')

    for keyword in major_keywords:
        if keyword.lower() in doc.text.lower():
            return keyword

    return ""
# --------------------------------------------------------------------------------

# --------------------------------Extract Experience-------------------------------
def extract_experience(doc):
    verbs = [token.text for token in doc if token.pos_ == 'VERB']

    senior_keywords = ['lead', 'manage', 'direct', 'oversee', 'supervise', 'orchestrate', 'govern']
    mid_senior_keywords = ['develop', 'design', 'analyze', 'implement', 'coordinate', 'execute', 'strategize']
    mid_junior_keywords = ['assist', 'support', 'collaborate', 'participate', 'aid', 'facilitate', 'contribute']
    
    if any(keyword in verbs for keyword in senior_keywords):
        level_of_experience = "Senior"
    elif any(keyword in verbs for keyword in mid_senior_keywords):
        level_of_experience = "Mid-Senior"
    elif any(keyword in verbs for keyword in mid_junior_keywords):
        level_of_experience = "Mid-Junior"
    else:
        level_of_experience = "Entry Level"

    suggested_position = suggest_position(verbs)

    return {
        'level_of_experience': level_of_experience,
        'suggested_position': suggested_position
    }

# --------------------------------------------------------------------------------


# -----------------------------------Suggestions----------------------------------
def load_positions_keywords(file_path):
    positions_keywords = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            position = row['position']
            keywords = [keyword.lower()
                        for keyword in row['keywords'].split(',')]
            positions_keywords[position] = keywords
    return positions_keywords


def suggest_position(verbs):
    positions_keywords = load_positions_keywords('data/position.csv')
    verbs = [verb.lower() for verb in verbs]
    for position, keywords in positions_keywords.items():
        if any(keyword in verbs for keyword in keywords):
            return position

    return "Position Not Identified"


def extract_resume_info_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return nlp(text)


def show_colored_skills(skills):
    if not skills or len(skills) == 0:
        st.info("📭 No skills found in the resume. Please ensure your resume contains technical skills.")
        return
    
    # Filter out any remaining invalid skills
    valid_skills = [skill for skill in skills if is_valid_skill(skill)]
    
    if not valid_skills:
        st.info("📭 No valid skills found after filtering. Please check your resume format.")
        return
    
    # Display skills as badges
    skills_html = " ".join([f'<span class="skill-badge">{skill}</span>' for skill in valid_skills])
    st.markdown(f"""
    <div class="info-card">
        <h4 style="color: #667eea;">🛠️ Skills Found ({len(valid_skills)})</h4>
        <div style="margin-top: 1rem; line-height: 2.5;">{skills_html}</div>
    </div>
    """, unsafe_allow_html=True)


def calculate_resume_score(resume_info):
    score = 0
    if resume_info['first_name'] and resume_info['last_name']:
        score += 25
    if resume_info['email']:
        score += 25
    if resume_info['degree_major']:
        score += 25
    if resume_info['skills']:
        score += 25
    return score


def extract_resume_info(doc):
    first_lines = '\n'.join(doc.text.splitlines()[:10])
    first_name, last_name = extract_name(doc)
    email = extract_email(doc)
    skills = extract_skills(doc)
    degree_major = extract_major(doc)
    experience = extract_experience(doc)

    return {'first_name': first_name, 'last_name': last_name, 'email': email, 'degree_major': degree_major, 'skills': skills, 'experience': experience}


def suggest_skills_for_job(desired_job):
    job_skills_mapping = {}
    
    with open('data/sugestedSkills.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            job_title = row[0].lower()
            skills = row[1:]
            job_skills_mapping[job_title] = skills
    
    desired_job_lower = desired_job.lower()
    if desired_job_lower in job_skills_mapping:
        suggested_skills = job_skills_mapping[desired_job_lower]
        return suggested_skills
    else:
        return []


'''
def show_pdf(uploaded_file):
    try:
        with open(uploaded_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    except AttributeError:
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

'''
