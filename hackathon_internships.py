import streamlit as st
import requests
from openai import OpenAI
import pandas as pd
import datetime
import json
import re

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

# Constants
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# ----------- Geocoding ------------
def geocode_location(location: str):
    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={"q": location, "format": "json", "limit": 1},
            headers={"User-Agent": "streamlit-app"}
        )
        if resp.ok and resp.json():
            data = resp.json()[0]
            return float(data["lat"]), float(data["lon"]), data.get("display_name", location)
    except Exception:
        return None, None, location
    return None, None, location

# ----------- Parse JSON from GPT response ------------
def extract_json_from_response(response_text: str):
    try:
        # Match everything inside square brackets (the JSON list)
        json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except Exception as e:
        st.error(f"⚠️ Error extracting JSON: {e}")
    return []

# ----------- Hackathon Generator ------------
def get_hackathons_from_openai(location: str) -> list:
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d, %Y")

    prompt = f"""
You are a hackathon event assistant. Generate a **fictional but realistic** list of upcoming hackathons in or near **{location}** after **{formatted_date}**.

Each hackathon should have:
- Name
- Approximate date (AFTER {formatted_date})
- 1–2 sentence description

Return only the JSON list:
[
  {{"name": "...", "date": "...", "description": "..."}} ,
  ...
]
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate realistic hackathon data in JSON format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.9,
    )
    return extract_json_from_response(response.choices[0].message.content.strip())

# ----------- Internship Generator ------------
def get_internships_from_openai(location: str, domain: str) -> list:
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d, %Y")

    prompt = f"""
You are a career placement assistant. Generate a **fictional but realistic** list of upcoming internship opportunities in **{domain}** near **{location}**, starting after **{formatted_date}**.

Each internship should include:
- Company name
- Internship title
- Start month
- Short 1-2 line description

Return only the JSON list:
[
  {{"company": "...", "title": "...", "start": "...", "description": "..."}} ,
  ...
]
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate realistic internship data in JSON format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.9,
    )
    return extract_json_from_response(response.choices[0].message.content.strip())

# ----------- Streamlit App ------------
def run():
    st.set_page_config(page_title="🏁 Hackathons & Internships", page_icon="🏁")
    st.title("🏁 Hackathons & Internships Explorer")

    # 📝 Functionality Description
    st.markdown("""
Welcome to the **Hackathons & Internships Explorer**! 🚀

This AI-powered tool helps you discover **fictional but realistic**:
- 🏆 Upcoming **hackathons** in your city or country
- 💼 **Internship opportunities** in your chosen domain

Just enter your location and domain, and click "Find Opportunities".
    """)

    # 💄 Styling
    st.markdown("""
        <style>
        .card {
            background-color: #f9f9f9;
            border-left: 6px solid #4CAF50;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .subtitle {
            font-size: 16px;
            color: #555;
        }
        .desc {
            font-size: 15px;
            color: #444;
        }
        </style>
    """, unsafe_allow_html=True)

    # 📍 Input Fields
    location_input = st.text_input("📍 Enter your location:", value="India")
    domain_input = st.selectbox("💼 Select your domain of interest:", [
        "AI/ML", "Web Development", "Cybersecurity", "Data Science", "Cloud Computing", "Blockchain", "UI/UX Design"
    ])

    if st.button("🔍 Find Opportunities"):
        lat, lon, resolved_location = geocode_location(location_input)
        if lat is None or lon is None:
            st.error("❌ Could not determine location. Please try again.")
            return

        st.success(f"📌 Location found: **{resolved_location}** (Lat: {lat:.2f}, Lon: {lon:.2f})")
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

        with st.spinner("🔎 Searching for hackathons..."):
            hackathons = get_hackathons_from_openai(resolved_location)

        with st.spinner("🔎 Searching for internships..."):
            internships = get_internships_from_openai(resolved_location, domain_input)

        # 🏆 Hackathon Results
        if hackathons:
            st.markdown(f"### 🏆 Upcoming Hackathons (after {datetime.date.today().strftime('%B %d, %Y')})")
            for h in hackathons:
                st.markdown(f"""
                <div class="card">
                    <div class="title">🚀 {h.get("name", "Untitled Hackathon")}</div>
                    <div class="subtitle">📅 {h.get("date", "TBD")}</div>
                    <div class="desc">{h.get("description", "")}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("😕 No hackathons found. Try a different location.")

        # 💼 Internship Results
        if internships:
            st.markdown(f"### 💼 Internship Opportunities in **{domain_input}**")
            for i in internships:
                st.markdown(f"""
                <div class="card">
                    <div class="title">🏢 {i.get("company", "Unnamed Company")} – {i.get("title", "")}</div>
                    <div class="subtitle">🗓️ Starts: {i.get("start", "TBD")}</div>
                    <div class="desc">{i.get("description", "")}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("😕 No internships found. Try a different domain or location.")

if __name__ == "__main__":
    run()
