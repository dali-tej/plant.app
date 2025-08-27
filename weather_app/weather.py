import streamlit as st
import requests
from streamlit_folium import st_folium
import folium
from folium.plugins import LocateControl

#loading key adn url
API_KEY = "b058c3260c006d722c4e8c2e968fd304"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

#making a function
def get_weather(city=None, lat=None, lon=None):
    if not city and (lat is None or lon is None): #checking for user input
        return {"error": "No location provided"}
    try:
        #importing inputs
        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
        else:  # use coordinates
            params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
        #sending request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        #getting response
        data = response.json()

        #loading data
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        city_name = data.get("name", "Unknown")

        return {
            "city": city_name,
            "weather": weather,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
        }
        #errors
    except requests.exceptions.HTTPError:
        return {"error": "City not found. Please try again."}
    except Exception as e:
        return {"error": str(e)}


# Background with css
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.pexels.com/photos/209831/pexels-photo-209831.jpeg?cs=srgb&dl=pexels-pixabay-209831.jpg&fm=jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#streamlit interface:

st.title("🌦️ Simple Weather App")

# Input choice
choice = st.radio("Choose input method:", ["Type city name", "Select on map"])

result = None

if choice == "Type city name":
    city = st.text_input("Enter a city:")
    if city:
        result = get_weather(city=city)

else:
    st.write("📍 Select a location on the map:")
    m = folium.Map(location=[36.8065, 10.1815], zoom_start=5)
    LocateControl().add_to(m)
    map_data = st_folium(m, width=700, height=450)


    if map_data and map_data["last_clicked"]:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        result = get_weather(lat=lat, lon=lon)

# Display results
if result:
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader(f"Weather in {result['city']}")
        st.write(f"**Condition:** {result['weather']}")
        st.write(f"**Temperature:** {result['temp']}°C (feels like {result['feels_like']}°C)")

        st.write(f"**Humidity:** {result['humidity']}%")
