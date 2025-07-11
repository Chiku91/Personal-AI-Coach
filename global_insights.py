import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from openai import OpenAI
import datetime

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_key"])

# -------------------------------
# Geocoding: Nominatim OpenStreetMap
# -------------------------------
def geocode_location(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "global-insights-app"}
    try:
        resp = requests.get(url, params=params, headers=headers)
        if resp.ok and resp.json():
            result = resp.json()[0]
            return float(result["lat"]), float(result["lon"]), result["display_name"]
    except Exception:
        return None, None, None
    return None, None, None

# -------------------------------
# GPT-4 Prompt for Market Insights
# -------------------------------
def get_global_insights(lat, lon, location_name):
    prompt = f"""
You are a global tech market analyst.

Provide industry-specific job market insights for the region: {location_name} (Latitude: {lat}, Longitude: {lon}).

Include:
- High-demand technologies and skills in that region
- Hiring trends and dominant industries
- Opportunities for software engineers or tech graduates
- Remote work and freelance job availability
- Any major companies or job platforms active there

Format the answer as a clear markdown summary.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in global employment trends."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# -------------------------------
# Streamlit App
# -------------------------------
def run():
    st.set_page_config(page_title="🌐 Global Insights", page_icon="🌍")
    st.title("🌐 Global Skill Demand & Job Market Insights")

    # 📘 App Description
    st.markdown("""
    Welcome to the **Global Insights Explorer** 🌍

    This AI-powered tool helps you explore **regional job market trends and high-demand tech skills** around the world.

    🔍 **What you can do here:**
    - Search for a location (e.g., "Bangalore", "London", or "Silicon Valley")
    - Click on the map to choose any custom region
    - Get an AI-generated report with:
      - Most in-demand technologies & skills
      - Hiring trends & dominant industries
      - Opportunities for software engineers & tech grads
      - Remote & freelance job market potential
      - Key employers & platforms in the region

    Use this to discover where your skills are needed, where to grow professionally, or where to target remote opportunities!
    """)

    # Session defaults
    default_values = {
        "lat": 28.6139,
        "lon": 77.2090,
        "address": "New Delhi, India",
        "clicked": False,
        "insights": "",
        "last_updated": None,
    }
    for key, val in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # 🌍 Search for a location
    location_input = st.text_input("📍 Search a location (e.g., Berlin, Silicon Valley, Tokyo):")

    if location_input:
        lat, lon, address = geocode_location(location_input)
        if lat and lon:
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.address = address
            st.session_state.clicked = True
        else:
            st.error("❌ Location not found. Please try another place.")

    # 🗺️ Render the map
    map_obj = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=6)
    folium.Marker(
        location=[st.session_state.lat, st.session_state.lon],
        tooltip="📍 Selected Location",
        popup=st.session_state.address,
        icon=folium.Icon(color="red", icon="briefcase")
    ).add_to(map_obj)

    click_data = st_folium(map_obj, height=500, width=700)

    if click_data and click_data.get("last_clicked"):
        clicked_lat = click_data["last_clicked"]["lat"]
        clicked_lon = click_data["last_clicked"]["lng"]
        st.session_state.lat = clicked_lat
        st.session_state.lon = clicked_lon
        st.session_state.address = f"Lat: {clicked_lat:.5f}, Lon: {clicked_lon:.5f}"
        st.session_state.clicked = True

    # 📈 Button to trigger insights
    if st.button("📈 Get Global Insights"):
        if not st.session_state.clicked:
            st.warning("Please select or search a location.")
        else:
            with st.spinner("Fetching global insights..."):
                try:
                    st.session_state.insights = get_global_insights(
                        st.session_state.lat,
                        st.session_state.lon,
                        st.session_state.address,
                    )
                    st.session_state.last_updated = datetime.datetime.now()
                except Exception as e:
                    st.error(f"⚠️ Failed to fetch insights: {e}")

    # 📊 Show insights
    if st.session_state.insights:
        st.markdown(f"### 📍 Insights for: **{st.session_state.address}**")
        if st.session_state.last_updated:
            st.caption(f"🕒 Last checked: {st.session_state.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(st.session_state.insights)

# Run the app
if __name__ == "__main__":
    run()
