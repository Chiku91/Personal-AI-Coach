import streamlit as st
import requests
from openai import OpenAI
import pandas as pd
import datetime

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

# ----------- AI Hackathon Generator ------------
def get_hackathons_from_openai(location: str) -> list:
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d, %Y")  # e.g., June 27, 2025

    prompt = f"""
You are a hackathon event assistant. Generate a **fictional but realistic** list of upcoming hackathons in or near **{location}** after **{formatted_date}** (today).

Each hackathon should have:
- Name
- Approximate date (AFTER {formatted_date})
- 1–2 sentence description

DO NOT include website or registration links. Return the output as JSON list of dictionaries like:
[
  {{"name": "...", "date": "...", "description": "..."}},
  ...
]
Return only the JSON list.
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

    try:
        hackathon_list = eval(response.choices[0].message.content.strip())
        return hackathon_list
    except Exception as e:
        st.error(f"⚠️ Failed to parse hackathon list: {e}")
        return []

# ----------- Streamlit App ------------
def run():
    st.set_page_config(page_title="🏁 Hackathons & Internships", page_icon="🏁")
    st.title("🏁 Hackathons & Internships Explorer")
    st.markdown("Discover exciting upcoming hackathons in your region and start building something amazing!")

    st.markdown("""
        <style>
        .hackathon-card {
            background-color: #f9f9f9;
            border-left: 6px solid #4CAF50;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .hackathon-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .hackathon-date {
            font-size: 16px;
            color: #555;
        }
        .hackathon-desc {
            font-size: 15px;
            color: #444;
        }
        </style>
    """, unsafe_allow_html=True)

    location_input = st.text_input("📍 Enter your location (city, state, or country):", value="India")

    if st.button("🔍 Find Events"):
        lat, lon, resolved_location = geocode_location(location_input)
        if lat is None or lon is None:
            st.error("❌ Could not determine location. Please try again.")
            return

        st.success(f"📌 Location found: **{resolved_location}** (Lat: {lat:.2f}, Lon: {lon:.2f})")
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}))

        with st.spinner("🔎 Finding nearby hackathons..."):
            hackathons = get_hackathons_from_openai(resolved_location)
            if hackathons:
                st.markdown(f"### 🏆 Hackathons After {datetime.date.today().strftime('%B %d, %Y')}")
                for hack in hackathons:
                    st.markdown(f"""
                        <div class="hackathon-card">
                            <div class="hackathon-title">🚀 {hack.get("name", "Untitled Hackathon")}</div>
                            <div class="hackathon-date">📅 {hack.get("date", "TBD")}</div>
                            <div class="hackathon-desc">{hack.get("description", "")}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("😕 No hackathons found. Try another location or check later.")

if __name__ == "__main__":
    run()
