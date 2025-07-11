import streamlit as st
import json
from openai import OpenAI
from streamlit_lottie import st_lottie
from fpdf import FPDF
import plotly.graph_objects as go

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["openai_key"])

# Load Lottie
def load_lottiefile(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Generate roadmap chart
def generate_roadmap_chart(level="Beginner"):
    skills = ["Python", "Machine Learning", "Deep Learning", "Cloud Deployment", "AI Ethics"]
    beginner = [90, 60, 40, 30, 20]
    expert = [100, 95, 90, 85, 70]
    y_data = beginner if level == "Beginner" else expert

    fig = go.Figure()
    fig.add_trace(go.Bar(x=skills, y=y_data, name=f"{level} Roadmap", marker_color='indigo'))
    fig.update_layout(
        title=f"{level} Skill Roadmap",
        xaxis_title="Skill",
        yaxis_title="Proficiency (%)",
        height=400
    )
    return fig

# Generate markdown career insights
def get_career_insights(domain, country):
    prompt = f"""
You are a career counselor. For the industry/domain "{domain}" in "{country}", provide:

1. 5 relevant career paths (job title + 1-line description + 3-5 key skills)
2. Top global and country-specific companies hiring
3. Close with a tip encouraging users to explore local job platforms

Format clearly in markdown with headings and bullet points.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a career guidance expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Export as PDF
def generate_pdf(text_md):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    cleaned = text_md.encode("ascii", "ignore").decode()
    pdf.multi_cell(0, 10, cleaned)
    path = "/mnt/data/career_insights.pdf"
    pdf.output(path)
    return path

# Export as Markdown
def generate_md(text_md):
    path = "/mnt/data/career_insights.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text_md)
    return path

# Main App
def run():
    st.set_page_config("Career Path Explorer", "🚀")
    st.title("🚀 Career Path Explorer")

    # 🎞️ Lottie Animation
    try:
        lottie = load_lottiefile("animations/Animation - 1749285017326.json")
        st_lottie(lottie, height=200)
    except:
        st.info("🎞️ Animation not found.")

    # 📝 App Description
    st.markdown("""
Welcome to the **Career Path Explorer**! 🚀  
This intelligent tool helps you explore career opportunities and growth plans tailored to your interests and location.

💡 **What this tool does**:
- Provides **AI-generated career insights** based on your domain (e.g. AI, Cybersecurity)
- Highlights **top job roles**, key skills, and hiring companies in your selected country
- Shows a **visual skill roadmap** based on your experience level (Beginner/Expert)
- Lets you **download insights** as PDF or Markdown for future reference

🌍 Ideal for students, professionals, and job seekers who want to:
- Discover trending career paths
- Upskill with a structured roadmap
- Find region-specific hiring info
- Prepare strategically for their next big move

Simply enter your domain and country below to begin!
    """)

    # 📌 User Inputs
    domain = st.text_input("Enter domain (e.g. AI, Cybersecurity, Web Dev):")
    countries = ["India", "USA", "Germany", "Canada", "Japan", "Remote"]
    country = st.selectbox("🌍 Select Country:", countries)
    roadmap_level = st.radio("🎯 Choose Roadmap Level:", ["Beginner", "Expert"], horizontal=True)

    # 🚀 Generate Insights Button
    if st.button("Generate Career Insights"):
        with st.spinner("🔎 Fetching results..."):
            try:
                result_md = get_career_insights(domain, country)

                # 📘 Career Insights Section
                st.markdown("### 📘 Career Insights")
                st.markdown(result_md)

                # 📊 Roadmap Chart
                st.markdown("### 📊 Skill Roadmap")
                st.plotly_chart(generate_roadmap_chart(roadmap_level), use_container_width=True)

                # 📎 Download Options
                st.markdown("### 📎 Download")
                col1, col2 = st.columns(2)
                with col1:
                    pdf_file = generate_pdf(result_md)
                    st.download_button("📄 Download PDF", open(pdf_file, "rb"), "career_insights.pdf", mime="application/pdf")
                with col2:
                    md_file = generate_md(result_md)
                    st.download_button("📝 Download Markdown", open(md_file, "rb"), "career_insights.md", mime="text/markdown")

            except Exception as e:
                st.error(f"Error generating results: {e}")

if __name__ == "__main__":
    run()
