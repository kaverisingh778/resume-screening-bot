import streamlit as st
import PyPDF2
import docx  # Ensure python-docx is installed
import nltk
import re
from nltk.corpus import stopwords

# Download stopwords only
nltk.download('stopwords')

# ----------- Function to extract resume text -----------
def extract_text(uploaded_file):
    text = ""
    if uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    elif uploaded_file.name.endswith('.docx'):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = "Unsupported file type."
    return text

# ----------- Function to clean resume text without nltk tokenizer -----------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', '', text)  # Remove special characters
    tokens = text.lower().split()  # Simple split on spaces
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

# ----------- Function to load job keywords -----------
def load_keywords():
    with open("job_keywords.txt", "r") as f:
        return [line.strip().lower() for line in f.readlines()]

# ----------- Function to match keywords -----------
def match_resume(cleaned_resume, keywords):
    matched = [kw for kw in keywords if kw in cleaned_resume]
    match_percent = (len(matched) / len(keywords)) * 100
    return matched, match_percent

# ----------- Streamlit UI -----------
st.set_page_config(page_title="Resume Screening Bot", layout="centered")

st.title("📄 Resume Screening Bot")
st.write("Upload your resume and see how well it matches the job requirements!")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

if uploaded_file is not None:
    with st.spinner('Reading your resume...'):
        resume_text = extract_text(uploaded_file)
        cleaned_resume = clean_text(resume_text)
        keywords = load_keywords()
        matched, score = match_resume(cleaned_resume, keywords)

    st.success("✅ Resume processed!")

    st.subheader("📊 Match Result")
    st.write(f"**Match Score:** `{score:.2f}%`")

    st.markdown("**✅ Matched Keywords:**")
    st.write(', '.join(matched) if matched else "No keywords matched 😢")

    st.markdown("**❌ Missing Keywords:**")
    missing = list(set(keywords) - set(matched))
    st.write(', '.join(missing) if missing else "Perfect match! 🎯")

    st.markdown("---")
    if score >= 70:
        st.success("🎉 Great! Your resume is a good match.")
    elif score >= 40:
        st.warning("⚠️ Your resume has some relevant skills. Improve it by adding more.")
    else:
        st.error("❌ Resume not a good match. Consider updating it with more relevant keywords.")


