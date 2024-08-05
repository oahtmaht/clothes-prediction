import streamlit as st
import pickle
import json
from flask import Flask, request, jsonify
from threading import Thread

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

# Function to predict size
def predict_size(height, weight, gender):
    gender_male = 1 if gender == "male" else 0
    gender_female = 1 if gender == "female" else 0

    features = [height, weight, gender_male, gender_female]
    prediction = model.predict([features])
    predicted_size = reverse_size_mapping[prediction[0]]

    return {"predicted_size": predicted_size}

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    height = data['height']
    weight = data['weight']
    gender = data['gender']
    result = predict_size(height, weight, gender)
    return jsonify(result)

def run_flask():
    app.run(port=5000)

# Start Flask server in a separate thread
thread = Thread(target=run_flask)
thread.start()

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
        result = predict_size(height, weight, gender)
        st.success(f"The fit clothes size for you is: {result['predicted_size']}")