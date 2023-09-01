import streamlit as st
import re
import nltk
import spacy
from pdfminer.high_level import extract_text

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Regular expressions for email and phone number extraction
PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]')
 
# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

# Skills database
SKILLS_DB = [
    'machine learning',
    'data science',
    'python',
    'word',
    'excel',
    'english',
    'java',
    'c++',
    'javascript',
    'web development',
    'sql',
    'communication',
    'problem solving',
    'teamwork',
    'leadership',
    'project management',
    'customer service',
    'sales',
    'marketing',
    'graphic design',
    'video editing',
    'networking',
    'cloud computing',
    'data analysis',
    'research',
    'teaching',
    'public speaking',
    # Add more skills here
]

# def extract_names(txt):
#     doc = nlp(txt)
#     person_names = []
    
#     for ent in doc.ents:
#         if ent.label_ == 'PERSON':
#             person_names.append(ent.text)
    
#     return person_names
def extract_names(txt):
    doc = nlp(txt)
    person_names = []
    
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            person_names.append(ent.text)
    
    # Remove duplicates and very short names
    cleaned_names = [name for name in person_names if len(name.split()) >= 2]
    
    return cleaned_names[0]

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
    if phone:
        number = ''.join(phone[0])
        if resume_text.find(number) == 0 and len(number) < 16:
            return number
    return None

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    filtered_tokens = [w for w in word_tokens if w.lower() not in stop_words and w.isalpha()]
    
    found_skills = set()
    
    for token in filtered_tokens:
        if token.lower() in SKILLS_DB:
            found_skills.add(token)
    
    return found_skills

def extract_education(input_text):
    education_keywords = ['education', 'degree', 'university', 'college']
    sentences = nltk.sent_tokenize(input_text)
    education_info = []
    for sent in sentences:
        for keyword in education_keywords:
            if keyword in sent.lower():
                education_info.append(sent)
                break
    return education_info

def main():
    st.title("Resume Parser")
    
    uploaded_file = st.file_uploader("Upload resume", type=["pdf"])
    
    if uploaded_file is not None:
        pdf_text = extract_text(uploaded_file)
        
        # Extract and print names
        names = extract_names(pdf_text)
        if names:
            st.write("Names:", names)
        
        # Extract and print phone number
        phone_number = extract_phone_number(pdf_text)
        if phone_number:
            st.write("Phone number:", phone_number)
        else:
            st.write("Phone number not found.")
        
        # Extract and print emails
        emails = extract_emails(pdf_text)
        if emails:
            st.write("Emails:", emails)
        else:
            st.write("No emails found.")
        
        # Extract and print skills
        skills = extract_skills(pdf_text)
        if skills:
            st.write("Skills:", skills)
        else:
            st.write("No skills found.")
        
        # Extract and print education
        education = extract_education(pdf_text)
        if education:
            st.write("Education:", education)
        else:
            st.write("No education information found.")

if __name__ == "__main__":
    main()
