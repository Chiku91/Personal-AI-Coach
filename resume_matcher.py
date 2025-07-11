import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

# Set Streamlit page configuration
st.set_page_config(page_title="Resume Matcher", page_icon="🧾")

# --------------------------
# Function: Extract text from uploaded PDF resume
# --------------------------
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# --------------------------
# Function: Match Resume with Job Description
# --------------------------
def match_resume_to_job(resume_text, job_desc):
    prompt = f"""
You are a professional job-matching assistant.

Compare the following resume with the job description. Perform:
- A percentage match (0-100%)
- List of matched skills
- List of missing skills
- Areas of improvement for the candidate

Resume:
\"\"\"{resume_text}\"\"\"

Job Description:
\"\"\"{job_desc}\"\"\"
"""
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a job-matching assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content

# --------------------------
# Streamlit App UI
# --------------------------
def run():
    st.title("🧾 Resume Matcher & Skill Analyzer")

    # 📘 App Description
    st.markdown("""
    This tool helps you **analyze your resume against any job description** using AI.
    
    🔍 **How it works:**
    - Upload your resume in PDF format.
    - Paste the job description in the text area.
    - Click on "Match Resume" to generate a detailed match report.

    ✅ The report includes:
    - Match percentage
    - Matched and missing skills
    - Suggestions for improvement

    Use this to fine-tune your resume and improve your job chances!
    """)

    uploaded_resume = st.file_uploader("📄 Upload your resume (PDF only)", type=["pdf"])
    job_desc = st.text_area("📝 Paste the Job Description Here:")

    resume_text = ""
    if uploaded_resume:
        with st.spinner("⏳ Extracting text from resume..."):
            resume_text = extract_text_from_pdf(uploaded_resume)
            st.success("✅ Resume text extracted.")

    if st.button("🔍 Match Resume"):
        if not resume_text or not job_desc:
            st.warning("⚠️ Please upload a resume and paste the job description.")
            return
        with st.spinner("🧠 Analyzing..."):
            try:
                result = match_resume_to_job(resume_text, job_desc)
                st.markdown("### 📊 Match Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Run the app
if __name__ == "__main__":
    run()
