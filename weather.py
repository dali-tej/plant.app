import streamlit as st
import requests
import sys

API_KEY = "b058c3260c006d722c4e8c2e968fd304" #API Key for verification
BASE_URL = "https://api.openweathermap.org/data/2.5/weather" #Base Weather Web URL

def get_weather(city):
    if not city:
        return {"error": "No city provided"}
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"} #Request parmaters
        response = requests.get(BASE_URL, params=params) #sending request
        response.raise_for_status() #Checks for the code status and raises an error if any
        data = response.json() #getting reponse in JSON format

        #getting the keys
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        #printing the keys
        print(f"\nWeather in {city.capitalize()}:")
        print(f"Condition: {weather}")
        print(f"Temperature: {temp}°C (feels like {feels_like}°C)")
        print(f"Humidity: {humidity}%\n")

        return {
            "weather": weather,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
        }

    #errors
    except requests.exceptions.HTTPError:
        print("City not found. Please try again.")
    except Exception as e:
        print("Something went wrong:", e)

# Add background image with CSS
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

# Streamlit UI
st.title("🌦️ Simple Weather App") #title of the app
city = st.text_input("Enter a city:") #input

if city:
    result = get_weather(city)
    if result and "error" in result: #checking for errors
        st.error(result["error"])
    elif result: #printing the result
        st.subheader(f"Weather in {city.capitalize()}")
        st.write(f"**Condition:** {result['weather']}")
        st.write(f"**Temperature:** {result['temp']}°C (feels like {result['feels_like']}°C)")
        st.write(f"**Humidity:** {result['humidity']}%")

