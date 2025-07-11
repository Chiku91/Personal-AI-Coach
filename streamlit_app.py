import streamlit as st
from streamlit_lottie import st_lottie
import json
import career_path_explorer
import course_recommendations
import global_insights
import hackathon_internships
import industry_trends
import mock_interview
import resume_matcher
import skill_builder
import streamlit.components.v1 as components

st.set_page_config(page_title="Career Coach", layout="wide")

# Load Lottie animation
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_career = load_lottiefile("animations/Animation - 1748757720975.json")

# Define app pages
PAGES = {
    "🏠 Home": None,
    "📄 Resume Matcher": resume_matcher,
    "🌍 Global Insights": global_insights,
    "📚 Course Recommendations": course_recommendations,
    "📊 Career Path Explorer": career_path_explorer,
    "🧠 Skill Builder": skill_builder,
    "🧪 Mock Interview Prep": mock_interview,
    "📅 Hackathons & Internships": hackathon_internships,
    "💡 Industry Trends": industry_trends,
}

# Sidebar navigation
st.sidebar.title("🧭 Navigate")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Main UI
if selection == "🏠 Home":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎓 **Career Coach for Students & Working Professionals**")
        st.markdown(
            """
            <div style='font-size:18px; line-height:1.6'>
            Whether you're a student preparing for your first job or a professional aiming for your next leap, this AI-powered career coach is designed for you.
            <br><br>
            🛠️ Unlock your full potential through tools that help you:
            <ul>
                <li>📄 Match your resume with job skills</li>
                <li>🌍 Discover global career insights</li>
                <li>📚 Get tailored course recommendations</li>
                <li>📊 Explore career paths in-demand</li>
                <li>🧠 Build and track in-demand skills</li>
                <li>🧪 Practice with mock interview questions</li>
                <li>📅 Find hackathons & internships</li>
                <li>💡 Stay ahead with industry trends</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st_lottie(lottie_career, height=350, key="career")

    # 🔍 Module descriptions
    st.markdown("---")
    st.markdown("## 🧭 Module Descriptions")
    st.markdown("""
### 📄 Resume Matcher  
Upload your resume and paste a job description to see how well they align. Get a match score, matched skills, missing skills, and improvement tips.

### 🌍 Global Insights  
Search any location worldwide to discover regional job opportunities, hiring trends, dominant tech domains, and in-demand skills using AI-generated data.

### 📚 Course Recommendations  
Enter skills or technologies you want to learn, and get a curated list of top online courses across platforms like Coursera, Udemy, edX, and more.

### 📊 Career Path Explorer  
Explore trending job roles in your domain and country, get AI-generated career insights, and view a visual skill roadmap for beginner or expert levels.

### 🧠 Skill Builder  
Upload your resume and let AI identify your strengths, gaps, and recommend a personalized upskilling plan with roadmap suggestions.

### 🧪 Mock Interview Prep  
Practice real-time technical or behavioral interview questions, answer them live, and get AI feedback including a score and areas to improve.

### 📅 Hackathons & Internships  
Find upcoming (fictional yet realistic) hackathons and internships in your location and tech domain, powered by AI event generation.

### 💡 Industry Trends  
Explore current industry trends, top companies, technologies in demand, and hiring patterns in a specific region using location-aware analysis.
    """)

else:
    page = PAGES[selection]
    if hasattr(page, "run") and callable(page.run):
        page.run()
    else:
        st.error(f"The page '{selection}' doesn't have a `run()` function.")
