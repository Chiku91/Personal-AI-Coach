import streamlit as st
from openai import OpenAI
import datetime
import re
import json
from streamlit_lottie import st_lottie

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

# Load Lottie animation
def load_lottie(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_json = load_lottie("animations/Animation - 1749286005992.json")

# Generate unique interview questions
def generate_questions(interview_type: str) -> list[str]:
    prompt = f"""You are an HR professional. Generate exactly ten {interview_type.lower()} interview questions suitable for final-year computer science/IT engineering students. Return them as a numbered list. Make the questions unique each time."""
    
    response = client.chat.completions.create(
        model="gpt-4",  # Use gpt-4 for better coherence
        messages=[
            {"role": "system", "content": "You are a professional interviewer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.8,
    )

    questions_text = response.choices[0].message.content.strip()
    return [re.sub(r"^\d+\.\s*", "", q).strip() for q in questions_text.splitlines() if q.strip()]

# Get AI feedback on Q&A
def get_feedback(questions, answers) -> str:
    qa_block = "\n\n".join(f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(zip(questions, answers)))
    prompt = f"""You are a seasoned technical interviewer. Review the following interview responses and provide:

1. Strengths of the candidate's answers  
2. Areas of improvement  
3. A rating out of 10 for each answer  

Interview Q&A:
{qa_block}

Return feedback in this format:
Question 1 Feedback (rating x/10): ...
Question 2 Feedback (rating x/10): ...
(continue for all)
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and objective interview evaluator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Streamlit App Logic
def run():
    st.set_page_config(page_title="Mock Interview", page_icon="🎤")
    st.title("🎤 Mock Interview Practice with AI")

    # 🔍 Functionality Description
    st.markdown("""
Welcome to the **Mock Interview Practice Tool**! 🎯  
This AI-powered assistant helps you prepare for job interviews by simulating a real Q&A session and offering detailed feedback.

💡 **What you can do here**:
- Choose your interview type (Technical or Behavioral)
- Get a fresh set of **10 interview questions**
- Write and reflect on your answers directly in the app
- Receive **AI-generated feedback** with:
  - Strengths in your responses
  - Areas for improvement
  - Score out of 10 for each answer

🧑‍💻 Ideal for:
- Final-year students in computer science/IT
- Job seekers looking to refine their responses
- Anyone practicing for mock or real interviews

Let’s help you build interview confidence — one question at a time!
""")

    # Layout: question type and animation side by side
    st.markdown("""
        <style>
            .container {display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; margin-bottom: 1.5rem;}
            .left-box, .right-box {flex: 1 1 300px;}
            .stButton > button {width: 100%;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="left-box">', unsafe_allow_html=True)

    interview_type = st.radio("Choose your interview focus:", ["Technical", "Behavioral"], horizontal=True)
    if st.button("🎯 Generate Interview Questions"):
        st.session_state.questions = generate_questions(interview_type)
        st.session_state.start_time = datetime.datetime.now()
        st.session_state.feedback = None

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="right-box">', unsafe_allow_html=True)
    st_lottie(lottie_json, height=220, key="mock_lottie")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Display questions & text areas
    if "questions" in st.session_state:
        st.subheader("📋 Your Mock Interview Questions")
        answers = []
        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}: {q}**")
            answers.append(st.text_area("✍️ Your Answer:", key=f"ans_{i}", height=120))

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("📝 Submit Answers for Feedback"):
                st.session_state.feedback = get_feedback(st.session_state.questions, answers)
        with col2:
            if "start_time" in st.session_state:
                elapsed = datetime.datetime.now() - st.session_state.start_time
                st.info(f"⏱️ Time Elapsed: {elapsed.seconds // 60} min {elapsed.seconds % 60} sec")

    # Feedback section
    if st.session_state.get("feedback"):
        st.markdown("### 🧠 Interview Feedback")
        st.markdown(st.session_state.feedback)

if __name__ == "__main__":
    run()
