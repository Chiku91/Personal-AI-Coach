import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import json
from streamlit_lottie import st_lottie

# Load OpenAI API key from secrets
client = OpenAI(api_key=st.secrets["openai_key"])

# ---------- Resume PDF Text Extraction ----------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

# ---------- AI Resume Analysis ----------
def analyze_resume_content(resume_text):
    prompt = f"""
You are a career guidance expert.

Analyze the following resume and provide:
1. Top 5 key strengths
2. Top 3 gaps or weaknesses
3. A personalized learning roadmap with upskilling suggestions

Resume:
\"\"\"{resume_text}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and insightful AI career coach."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content

# ---------- Optional: Load Lottie animation ----------
def load_lottiefile(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- UI Entry Point ----------
def run():
    st.set_page_config(page_title="Skill Builder", page_icon="🛠️")
    st.title("🛠️ Resume-Based Skill Builder")

    # 🔍 Module Description
    st.markdown("""
Welcome to the **AI-powered Skill Builder Tool**! 🧠  
Upload your resume and let AI analyze your strengths, weaknesses, and recommend a personalized **learning roadmap** to help you grow professionally.

💡 **What you’ll get:**
- ✅ Top 5 strengths identified from your resume
- ⚠️ 3 skill gaps or areas needing improvement
- 📘 Tailored learning suggestions to upskill and stay industry-ready

This is ideal for:
- Students looking to improve their resume before applying
- Professionals aiming to pivot or level up in their career
- Anyone curious about where they stand and how to grow

Get started by uploading your resume below! ⬇️
""")

    # Load and show Lottie animation
    try:
        lottie_resume = load_lottiefile("animations/Animation - 1749285315567.json")
        st_lottie(lottie_resume, speed=1, loop=True, quality="high", height=250)
    except Exception:
        st.info("⚠️ Animation could not be loaded.")

    # 📄 Upload Resume
    uploaded = st.file_uploader("📄 Upload Your Resume (PDF format)", type=["pdf"])

    # 🔍 Analyze Button
    if uploaded and st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing resume content..."):
            try:
                resume_text = extract_text_from_pdf(uploaded)
                if len(resume_text) < 100:
                    st.warning("⚠️ The resume text seems too short. Please upload a detailed resume.")
                    return
                analysis = analyze_resume_content(resume_text)
                st.markdown("### ✅ Career Analysis Result")
                st.markdown(analysis)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# 🔁 Run the App
if __name__ == "__main__":
    run()
