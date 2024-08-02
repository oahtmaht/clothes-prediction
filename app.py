import streamlit as st
import pickle
import json

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Load the pre-trained model
with open(config['model_path'], 'rb') as file:
    model = pickle.load(file)

# Original label encoding mapping
size_mapping = config['size_mapping']
# Create reverse mapping
reverse_size_mapping = {v: k for k, v in size_mapping.items()}

# Streamlit interface
st.title("Clothes Size Prediction")

st.write("Welcome to the Clothes Size Prediction!")

height = st.number_input("Height (cm)", min_value=0)
weight = st.number_input("Weight (kg)", min_value=0)
gender = st.selectbox("Gender", ["male", "female"])

if st.button("Predict"):
    if height <= 0 or weight <= 0:
        st.error("Height and weight must be positive numbers.")
    else:
        gender_male = 1 if gender == 'male' else 0
        gender_female = 1 if gender == 'female' else 0

        features = [height, weight, gender_male, gender_female]
        prediction = model.predict([features])
        predicted_size = reverse_size_mapping[prediction[0]]

        st.success(f"The fit clothes size for you is: {predicted_size}")