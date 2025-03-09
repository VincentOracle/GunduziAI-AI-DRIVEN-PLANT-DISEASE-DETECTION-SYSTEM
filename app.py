# Main Application

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Define the upload folder for images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load ML Model once (cached)
def load_model():
    model_path = "trained_model.h5"
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    return None

model = load_model()

# Helper function to check if the user is logged in
def is_logged_in():
    return 'email' in session and 'first_name' in session

@app.route("/")
def home():
    first_name = session.get('first_name', 'Guest')  # Default to 'Guest' if not logged in
    return render_template("index.html", first_name=first_name)

@app.route("/set_session", methods=["POST"])
def set_session():
    data = request.get_json()
    session['first_name'] = data.get('first_name')
    session['email'] = data.get('email')
    return jsonify({"success": True})

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = request.form.get('email')
        password = request.form.get('password')
        # Here you would typically validate the user's credentials
        # For now, we'll just set the session variables
        session['email'] = email
        # Fetch the first name from the database or session (if available)
        # For now, we'll simulate it by setting it to the email prefix
        session['first_name'] = email.split('@')[0]  
        # Simulate first name from email
        session['first_name'] = data.get('first_name')
        return redirect(url_for('home'))
    return render_template("login_signUp.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('home'))

# About Page (Public)
@app.route("/about")
def about():
    return render_template("about.html")

# Disease Recognition Page (Protected)
@app.route("/disease_recognition", methods=["GET", "POST"])
def disease_recognition():
    if not is_logged_in():
        return redirect(url_for('login'))
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"})
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "error": "No file selected"})
        
        if file:
            try:
                # Save the uploaded file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                # Process the image
                image = Image.open(filepath)
                image = image.resize((128, 128))  # Resize image to match model input size
                input_arr = tf.keras.preprocessing.image.img_to_array(image)
                img_array = np.array([input_arr])
                # Prediction
                prediction = model.predict(img_array)
                confidence = np.max(prediction) * 100  # Get confidence score
                # Actual labels from the 38 classes
                labels = [
                    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
                    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
                    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
                    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
                    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
                    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
                    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
                    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
                    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
                    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
                    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy'
                ]
                predicted_label = labels[np.argmax(prediction)]
                return jsonify({
                    "success": True,
                    "prediction": predicted_label,
                    "confidence": float(confidence),  # Convert to float for JSON serialization
                    "image_url": file.filename
                })
            except Exception as e:
                return jsonify({"success": False, "error": str(e)})
    return render_template("disease_recognition.html")

# Expert Consultation Page (Protected)
@app.route("/expert")
def expert():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("expert.html")

# User Dashboard Page (Protected)
@app.route("/user_dashboard")
def user_dashboard():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("user_dashboard.html")

# Contact Page (Protected)
@app.route("/contact")
def contact():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("contact.html")

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)