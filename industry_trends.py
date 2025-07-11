import streamlit as st
import requests
import folium
from openai import OpenAI
from streamlit_folium import st_folium
import datetime

# Initialize OpenAI
client = OpenAI(api_key=st.secrets["openai_key"])

# Geocoding with OpenStreetMap
def search_place(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "IndustryTrendsApp/1.0"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data["lat"]), float(data["lon"]), data.get("display_name", query)
    return None, None, None

# Fetch industry trends from OpenAI
def get_industry_trends(lat, lon):
    prompt = (
        f"You are a market analyst. Provide an engaging analysis of current industry trends "
        f"around latitude {lat} and longitude {lon}. Include:\n"
        f"- Key local companies and what domains they're in\n"
        f"- In-demand technologies and skills\n"
        f"- Job market status (growth, hiring freeze, remote trends, etc.)\n"
        f"- Career opportunities for tech graduates in the region\n"
        f"Use clear Markdown formatting and bullet points."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful industry trends assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Main Streamlit App
def run():
    st.set_page_config(page_title="📈 Industry Trends", page_icon="📊")

    st.markdown("""
        <style>
        .location-box {
            padding: 1rem;
            background-color: #f8f9fa;
            border-left: 4px solid #4CAF50;
            border-radius: 8px;
            margin-top: 1rem;
            font-size: 16px;
        }
        .trend-box {
            background: #f4f4f4;
            padding: 1.2rem;
            border-radius: 10px;
            border-left: 5px solid #3f51b5;
            margin-bottom: 1.5rem;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🌍 Industry Trends Explorer")

    # ✅ New Descriptive Text
    st.markdown("""
Welcome to the **Industry Trends Explorer**! 📊  
This tool helps you discover real-time insights into the tech industry based on your selected location.

💡 **What you can explore:**
- Key companies and industries active in the region  
- In-demand technologies and job market conditions  
- Opportunities for tech graduates  
- Remote work trends and regional hiring outlook

Just enter a city, region, or country below to get started. The map will update and you'll receive an AI-generated trend report tailored to that location.
    """)

    for key, default in {
        "lat": 28.6139,
        "lon": 77.2090,
        "address": "New Delhi, India",
        "trends": "",
        "clicked": False,
        "last_checked": None,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    place_search = st.text_input("📍 Enter a location (e.g., Bengaluru, London, California):")

    if place_search:
        lat, lon, address = search_place(place_search)
        if lat and lon:
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.address = address
            st.session_state.clicked = True
        else:
            st.warning("❌ Location not found. Please try again.")

    # Map
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)
    folium.Marker(
        location=[st.session_state.lat, st.session_state.lon],
        popup=st.session_state.address,
        tooltip="📍 Selected Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    st_folium(m, height=500, width=700)

    if st.button("📊 Show Industry Trends"):
        if not st.session_state.clicked:
            st.warning("Please enter a location or click on the map.")
        else:
            with st.spinner("Fetching data..."):
                try:
                    st.session_state.trends = get_industry_trends(
                        st.session_state.lat, st.session_state.lon
                    )
                    st.session_state.last_checked = datetime.datetime.now()
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.trends:
        st.markdown(f"""
        <div class="location-box">
            <b>📌 Trends for:</b> {st.session_state.address}<br>
            <small>🕒 Last updated: {st.session_state.last_checked.strftime('%A, %d %B %Y %I:%M %p')}</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""<div class="trend-box">{st.session_state.trends}</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
