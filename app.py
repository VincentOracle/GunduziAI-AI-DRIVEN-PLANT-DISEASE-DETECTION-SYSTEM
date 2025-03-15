
#  # Main Application


# from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from datetime import datetime
# import os
# import tensorflow as tf
# import numpy as np
# from PIL import Image

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Replace with a real secret key

# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:were8368@localhost/gunduziai'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Define the upload folder for images
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure the upload folder exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Load ML Model once (cached)
# def load_model():
#     model_path = "trained_model.h5"
#     if os.path.exists(model_path):
#         return tf.keras.models.load_model(model_path)
#     return None

# model = load_model()

# # Helper function to check if the user is logged in
# def is_logged_in():
#     return 'email' in session and 'first_name' in session

# # Database Models
# class Users(db.Model, UserMixin):
#     __tablename__ = 'users'
#     User_ID = db.Column(db.Integer, primary_key=True)
#     First_Name = db.Column(db.String(50), nullable=False)
#     Last_Name = db.Column(db.String(50), nullable=False)
#     Role = db.Column(db.String(50), nullable=False)
#     Phone_number = db.Column(db.Integer, nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Password = db.Column(db.String(100), nullable=False)

#     def get_id(self):
#         return self.User_ID

# class Plant_Images(db.Model):
#     __tablename__ = 'plant_images'  # Explicitly set the table name
#     Image_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     Upload_Date = db.Column(db.Date, nullable=False)
#     Image_URL = db.Column(db.String(200), nullable=False)
#     Quality_Status = db.Column(db.String(50), nullable=False)

# class Diseases(db.Model):
#     __tablename__ = 'diseases'
#     Disease_ID = db.Column(db.Integer, primary_key=True)
#     Disease_Name = db.Column(db.String(100), unique=True, nullable=False)
#     Symptoms = db.Column(db.String(200), nullable=False)
#     Severity_Level = db.Column(db.String(50), nullable=False)
#     Similar_Diseases = db.Column(db.String(200), nullable=False)

# class Diagnosis_Results(db.Model):
#     __tablename__ = 'diagnosis_results'
#     Result_ID = db.Column(db.Integer, primary_key=True)
#     Image_ID = db.Column(db.Integer, db.ForeignKey('plant_images.Image_ID'), nullable=False)
#     Disease_ID = db.Column(db.Integer, db.ForeignKey('diseases.Disease_ID'), nullable=False)
#     Predicted_Disease = db.Column(db.String(100), nullable=False)
#     Percentage_Confidence = db.Column(db.Float, nullable=False)
#     Diagnosis_Method = db.Column(db.String(50), nullable=False)
#     Diagnosis_Date = db.Column(db.Date, nullable=False)

# class Treatment_Recommendations(db.Model):
#     __tablename__ = 'treatment_recommendations'
#     Treatment_ID = db.Column(db.Integer, primary_key=True)
#     Disease_ID = db.Column(db.Integer, db.ForeignKey('diseases.Disease_ID'), nullable=False)
#     Created_Date = db.Column(db.Date, nullable=False)
#     Disease_Name = db.Column(db.String(100), nullable=False)
#     Preventive_Measures = db.Column(db.String(200), nullable=False)
#     Chemical_Treatments = db.Column(db.String(200), nullable=False)
#     Organic_Solutions = db.Column(db.String(200), nullable=False)
#     Best_Farming_Practices = db.Column(db.String(200), nullable=False)

# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     Feedback_ID = db.Column(db.Integer, primary_key=True)
#     User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
#     Diagnosis_ID = db.Column(db.Integer, db.ForeignKey('diagnosis_results.Result_ID'), nullable=False)
#     Feedback_Date = db.Column(db.Date, nullable=False)
#     Prediction_Accuracy = db.Column(db.Integer, nullable=False)
#     System_Rating = db.Column(db.Integer, nullable=False)
#     Feedback_Text = db.Column(db.String(200), nullable=False)

# # Create Database Tables
# with app.app_context():
#     db.create_all()

# # Routes
# @app.route("/")
# def home():
#     first_name = session.get('first_name', 'Guest')  # Default to 'Guest' if not logged in
#     return render_template("index.html", first_name=first_name)

# @app.route("/set_session", methods=["POST"])
# def set_session():
#     data = request.get_json()
#     session['first_name'] = data.get('first_name')
#     session['email'] = data.get('email')
#     return jsonify({"success": True})

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         first_name = request.form.get("first_name")
#         last_name = request.form.get("last_name")
#         role = request.form.get("user_role")
#         phone_number = request.form.get("phone_number")
#         email = request.form.get("email")
#         password = request.form.get("password")

#         # Check if the email already exists
#         if Users.query.filter_by(Email=email).first():
#             return jsonify({"success": False, "error": "Email already exists. Please use a different email."})

#         # Create a new user
#         new_user = Users(
#             First_Name=first_name,
#             Last_Name=last_name,
#             Role=role,
#             Phone_number=phone_number,
#             Email=email,
#             Password=password
#         )
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({"success": True})
#     return render_template("login_signUp.html")

# # Login Page
# # @app.route("/login", methods=["GET", "POST"])
# # def login():
# #     if request.method == "POST":
# #         email = request.form.get('email')
# #         password = request.form.get('password')

# #         # Check if user exists in the database
# #         user = Users.query.filter_by(Email=email, Password=password).first()
# #         if user:
# #             session['email'] = user.Email
# #             session['first_name'] = user.First_Name
# #             if user.Role == "Admin":
# #                 return redirect(url_for('admin_dashboard'))
# #             return redirect(url_for('home'))
# #         flash("Invalid email or password", "error")
# #     return render_template("login_signUp.html")
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")

#         # Check if user exists in the database
#         user = Users.query.filter_by(Email=email, Password=password).first()
#         if user:
#             session["email"] = user.Email
#             session["first_name"] = user.First_Name
#             if user.Role == "Admin":
#                 return jsonify({"success": True, "redirect": url_for("admin_dashboard")})
#             return jsonify({"success": True, "redirect": url_for("home")})
#         return jsonify({"success": False, "error": "Invalid email or password"})
#     return render_template("login_signUp.html")

# # Logout
# @app.route("/logout")
# def logout():
#     session.pop('email', None)
#     session.pop('first_name', None)
#     return redirect(url_for('home'))

# # Disease Recognition Page (Protected)
# @app.route("/disease_recognition", methods=["GET", "POST"])
# def disease_recognition():
#     if not is_logged_in():
#         return redirect(url_for('login'))
#     if request.method == "POST":
#         if "file" not in request.files:
#             return jsonify({"success": False, "error": "No file uploaded"})

#         file = request.files["file"]
#         if file.filename == "":
#             return jsonify({"success": False, "error": "No file selected"})

#         if file:
#             try:
#                 # Save the uploaded file
#                 filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#                 file.save(filepath)
#                 # Process the image
#                 image = Image.open(filepath)
#                 image = image.resize((128, 128))  # Resize image to match model input size
#                 input_arr = tf.keras.preprocessing.image.img_to_array(image)
#                 img_array = np.array([input_arr])
#                 # Prediction
#                 prediction = model.predict(img_array)
#                 confidence = np.max(prediction) * 100  # Get confidence score
#                 # Actual labels from the 38 classes
#                 labels = [
#                     'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_rust', 'Apple___healthy',
#                     'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
#                     'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
#                     'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
#                     'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
#                     'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
#                     'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
#                     'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
#                     'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
#                     'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
#                     'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
#                     'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
#                     'Tomato___healthy'
#                 ]
#                 predicted_label = labels[np.argmax(prediction)]
#                 return jsonify({
#                     "success": True,
#                     "prediction": predicted_label,
#                     "confidence": float(confidence),  # Convert to float for JSON serialization
#                     "image_url": file.filename
#                 })
#             except Exception as e:
#                 return jsonify({"success": False, "error": str(e)})
#     return render_template("disease_recognition.html")

# # Expert Consultation Page (Protected)
# @app.route("/expert")
# def expert():
#     if not is_logged_in():
#         return redirect(url_for('login'))
#     return render_template("expert.html")

# # User Dashboard Page (Protected)
# @app.route("/user_dashboard")
# def user_dashboard():
#     if not is_logged_in():
#         return redirect(url_for('login'))
#     return render_template("user_dashboard.html")

# # Admin Dashboard Page (Protected)
# @app.route("/admin_dashboard")
# def admin_dashboard():
#     if not is_logged_in() or session.get('first_name') != "Admin":
#         return redirect(url_for('login'))
#     return render_template("admin_dashboard.html")

# # Run the Flask App
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:were8368@localhost/gunduziai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Database Models
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    User_ID = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(50), nullable=False)
    Last_Name = db.Column(db.String(50), nullable=False)
    Role = db.Column(db.String(50), nullable=False)
    Phone_number = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.User_ID

class Plant_Images(db.Model):
    __tablename__ = 'plant_images'  # Explicitly set the table name
    Image_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
    Upload_Date = db.Column(db.Date, nullable=False)
    Image_URL = db.Column(db.String(200), nullable=False)
    Quality_Status = db.Column(db.String(50), nullable=False)

class Diseases(db.Model):
    __tablename__ = 'diseases'
    Disease_ID = db.Column(db.Integer, primary_key=True)
    Disease_Name = db.Column(db.String(100), unique=True, nullable=False)
    Symptoms = db.Column(db.String(200), nullable=False)
    Severity_Level = db.Column(db.String(50), nullable=False)
    Similar_Diseases = db.Column(db.String(200), nullable=False)

class Diagnosis_Results(db.Model):
    __tablename__ = 'diagnosis_results'
    Result_ID = db.Column(db.Integer, primary_key=True)
    Image_ID = db.Column(db.Integer, db.ForeignKey('plant_images.Image_ID'), nullable=False)
    Disease_ID = db.Column(db.Integer, db.ForeignKey('diseases.Disease_ID'), nullable=False)
    Predicted_Disease = db.Column(db.String(100), nullable=False)
    Percentage_Confidence = db.Column(db.Float, nullable=False)
    Diagnosis_Method = db.Column(db.String(50), nullable=False)
    Diagnosis_Date = db.Column(db.Date, nullable=False)

class Treatment_Recommendations(db.Model):
    __tablename__ = 'treatment_recommendations'
    Treatment_ID = db.Column(db.Integer, primary_key=True)
    Disease_ID = db.Column(db.Integer, db.ForeignKey('diseases.Disease_ID'), nullable=False)
    Created_Date = db.Column(db.Date, nullable=False)
    Disease_Name = db.Column(db.String(100), nullable=False)
    Preventive_Measures = db.Column(db.String(200), nullable=False)
    Chemical_Treatments = db.Column(db.String(200), nullable=False)
    Organic_Solutions = db.Column(db.String(200), nullable=False)
    Best_Farming_Practices = db.Column(db.String(200), nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    Feedback_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
    Diagnosis_ID = db.Column(db.Integer, db.ForeignKey('diagnosis_results.Result_ID'), nullable=False)
    Feedback_Date = db.Column(db.Date, nullable=False)
    Prediction_Accuracy = db.Column(db.Integer, nullable=False)
    System_Rating = db.Column(db.Integer, nullable=False)
    Feedback_Text = db.Column(db.String(200), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Routes
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
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "admintest@gmail.com" and password == "@Admin1234":
            session['email'] = email
            session['first_name'] = "Admin"
            return redirect(url_for('admin_dashboard'))

        # Check if user exists in the database
        user = Users.query.filter_by(Email=email, Password=password).first()
        if user:
            session['email'] = user.Email
            session['first_name'] = user.First_Name
            if user.Role == "Admin":
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        flash("Invalid email or password", "error")
    return render_template("login_signUp.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('home'))

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

# Admin Dashboard Page (Protected)
@app.route("/admin_dashboard")
def admin_dashboard():
    if not is_logged_in() or session.get('first_name') != "Admin":
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html")

# Sign-up Route
@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_role = request.form.get('user_role')
        phone_number = int(request.form.get('phone_number'))
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email already exists
        existing_user = Users.query.filter_by(Email=email).first()
        if existing_user:
            return jsonify({"success": False, "error": "Email already exists"})

        # Create new user
        new_user = Users(
            First_Name=first_name,
            Last_Name=last_name,
            Role=user_role,
            Phone_number=phone_number,
            Email=email,
            Password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid request"})

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)