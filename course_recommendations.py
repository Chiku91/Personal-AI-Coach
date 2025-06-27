import streamlit as st
import json
from openai import OpenAI
from streamlit_lottie import st_lottie

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

# Load Lottie animation
def load_lottiefile(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

# Streamlit App
def run():
    st.set_page_config(page_title="🎯 Course Recommendations", page_icon="🎓")
    st.markdown('<div style="text-align:center; max-width:700px; margin:auto;">', unsafe_allow_html=True)

    try:
        st_lottie(load_lottiefile("animations/Animation - 1749284783217.json"), height=160)
    except Exception:
        st.info("Lottie animation not loaded. Please check the file path.")

    st.title("🎯 Smart Course Recommendations")
    st.markdown("Enter any tech skills or topics to receive curated online course recommendations.")

    topics = st.text_input("📘 Enter topics (comma-separated):", placeholder="e.g., Flutter, Cybersecurity, Data Science")

    if st.button("📚 Get Recommendations") and topics.strip():
        prompt = f"""
You are an expert education counselor. Suggest 10 high-quality online courses based on the following topics: {topics}.

For each course, provide:
1. **Platform** (Coursera, Udemy, edX, etc.)
2. **Course Title** as a clickable Markdown link (use [Course Title](url) format)
3. A **short reason** why it's recommended.

Ensure recommendations are diverse and beginner-friendly unless the topic implies advanced expertise.
Format the response as a numbered markdown list.
"""
        with st.spinner("🔍 Searching top-rated courses..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",  # Or use gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are a helpful course recommender."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=1.0,
                )
                st.markdown("### 🧠 Top Course Recommendations")
                st.markdown(response.choices[0].message.content.strip())
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    run()
