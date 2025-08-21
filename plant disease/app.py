import streamlit as st
import joblib
import pandas as pd
import os

# Always get the current directory of app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model + encoder using absolute paths
model = joblib.load(os.path.join(BASE_DIR, "plant_disease_model.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR, "encoder.pkl"))

#encoder dict
categories_dict = {
    "Leaf_Color": {cat: i for i, cat in enumerate(encoder.categories_[0])},
    "Spots": {cat: i for i, cat in enumerate(encoder.categories_[1])}
}

#title of the app
st.title("🌱 Plant Disease Classifier")

#input widgets
leaf_color = st.selectbox("Leaf Color", list(categories_dict["Leaf_Color"].keys()))
spots = st.selectbox("Spots", list(categories_dict["Spots"].keys()))
moisture = st.slider("Moisture", 20, 90, 50)
temperature = st.slider("Temperature (°C)", 15, 35, 25)

#predict button
if st.button("Predict Disease"):
    input_df = pd.DataFrame({
        "Leaf_Color": [categories_dict["Leaf_Color"][leaf_color]],
        "Spots": [categories_dict["Spots"][spots]],
        "Moisture": [moisture],
        "Temperature": [temperature]
    })
    # prediction
    prediction = model.predict(input_df)[0]
    # prediction dispay
    st.success(f"Predicted Disease: {prediction}")
