# Personal-AI-Coach

# 🚀 ElevateU – Your Personal AI Career Coach

**ElevateU** is a smart, AI-powered career coaching web app built with **Streamlit** and **OpenAI**. It helps students, job seekers, and early professionals bridge the gap between their resume and the real-world job market. The goal is simple: **Elevate You** — your career, your skills, and your future.

## 🎯 Why ElevateU?

- No confusing career advice
- No generic suggestions
- Just intelligent, tailored guidance from the power of **AI**

## 🌟 Features

### 🧾 Resume Matcher
- Upload or paste your resume
- Powered by **OpenAI GPT-4**
- Compares your resume against any job description
- Shows:
  - ✅ Match percentage
  - 🔍 Missing skills
  - 🛠️ Areas to improve

### 🛠️ Skill Builder
- Upload resume as PDF
- Uses **OpenAI GPT-4** to:
  - Analyze strengths and weaknesses
  - Detect skill gaps
  - Recommend a custom learning roadmap

### 🎯 Course Recommendations
- Enter any keyword/topic (e.g., "Flutter", "Ethical Hacking")
- Uses **OpenAI GPT-4** to fetch top 10 online courses from platforms like Coursera, Udemy, edX
- Shows:
  - 📚 Platform name
  - 🔗 Clickable course title
  - 💡 Why it's recommended

### 🧭 Career Path Explorer
- Input any career goal (e.g., "AI Engineer", "Product Manager")
- Uses **OpenAI GPT-4** to generate:
  - 📈 Roadmap from beginner to expert
  - 📃 Required skills & certifications
  - 👨‍💻 Job roles & responsibilities
  - 🌐 Top hiring companies
  - 📊 Career path visual charts *(using Plotly)*

### 🎤 Mock Interview
- Choose between **Technical** or **Behavioral** interviews
- Generates **10 unique questions**
- Type your answers
- **OpenAI GPT-4** gives:
  - 💬 Feedback on each answer
  - ✅ Strengths
  - 🔴 Weaknesses
  - 🔢 Score out of 10

### 🏁 Hackathons & Internships
- Enter a location
- Uses **OpenAI GPT-4** to list upcoming hackathons nearby (post today’s date only)
- Shows:
  - 🏷️ Hackathon name
  - 📅 Dates (from current month onward)
  - 📝 Description

### 📈 Industry Trends
- Interactive **Streamlit + Folium** map
- Search or click anywhere on map
- **OpenAI GPT-4** generates region-specific insights:
  - 🏢 Local companies
  - 🔧 Technologies in demand
  - 📊 Hiring status
  - 🎓 Opportunities for tech graduates

## 🧠 Powered by OpenAI

| Feature               | OpenAI GPT Model Used | Purpose                                       |
|----------------------|-----------------------|-----------------------------------------------|
| Resume Matcher        | GPT-4                | Match %, missing skills, recommendations       |
| Skill Builder         | GPT-4                | Analyze resume, skill gaps, roadmap            |
| Course Recommender    | GPT-4                | Fetch and explain course suggestions           |
| Career Path Explorer  | GPT-4                | Generate roadmaps, skills, certifications      |
| Mock Interview        | GPT-4                | Create questions, give feedback                |
| Hackathons & Internships | GPT-4             | List realistic events near user’s location     |
| Industry Trends       | GPT-4                | Analyze job and tech trends by region          |


## 🔒 Secure Setup

- All API keys are stored securely in `.streamlit/secrets.toml`
- This file is excluded from Git using `.gitignore`
- Never expose your OpenAI API key publicly

Example `secrets.toml`:
```toml
openai_key = "sk-*************"
