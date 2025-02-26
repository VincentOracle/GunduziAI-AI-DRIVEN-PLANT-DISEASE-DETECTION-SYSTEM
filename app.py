
# Main flask Application

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, session, flash
import os
import tensorflow as tf
import numpy as np
import os
from PIL import Image

app = Flask(__name__)

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

# Home Page
@app.route("/")
def home():
    if 'first_name' not in session:
        return redirect(url_for('login'))
    
    return render_template("index.html", first_name=session['first_name'])

@app.route("/set_session", methods=["POST"])
def set_session():
    data = request.get_json()
    session['first_name'] = data['first_name']
    return jsonify({"success": True})

# Login Page
@app.route("/login")
def login():
    return render_template("login_signUp.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('first_name', None)
    return redirect(url_for('login'))

# Protected Routes
@app.route("/about")
def about():
    if 'first_name' not in session:
        return redirect(url_for('login'))
    return render_template("about.html")

@app.route("/disease_recognition", methods=["GET", "POST"])
def disease_recognition():
    if 'first_name' not in session:
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
                    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
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

# Experts page
@app.route("/expert")
def expert():
    if 'first_name' not in session:
        return redirect(url_for('login'))
    return render_template("expert.html")

# Contact page
@app.route("/contact")
def contact():
    if 'first_name' not in session:
        return redirect(url_for('login'))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)