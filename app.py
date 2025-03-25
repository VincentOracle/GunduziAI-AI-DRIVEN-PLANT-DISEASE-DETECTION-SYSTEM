# Main Application

from flask import Flask, render_template, request, redirect, send_from_directory, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct, text
import random  
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import tensorflow as tf
import numpy as np
from sqlalchemy import func
from PIL import Image
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0' # Disable oneDNN custom operations
tf.get_logger().setLevel('ERROR')  # Suppress TensorFlow warnings

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

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

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Helper function to check if the user is logged in
def is_logged_in():
    logged_in = 'email' in session and 'first_name' in session
    print(f"is_logged_in: {logged_in}, Session: {session}")
    return logged_in

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
    __tablename__ = 'plant_images'
    Image_ID = db.Column(db.Integer, primary_key=True)
    User_ID = db.Column(db.Integer, db.ForeignKey('users.User_ID'), nullable=False)
    Upload_Date = db.Column(db.Date, nullable=False)
    Image_URL = db.Column(db.String(200), nullable=False)
    Quality_Status = db.Column(db.String(50), nullable=False)

class Diseases(db.Model):
    __tablename__ = 'diseases'
    Disease_ID = db.Column(db.Integer, primary_key=True)
    Image_URL = db.Column(db.String(2000), nullable=False)
    Disease_Name = db.Column(db.String(2000), unique=False, nullable=False)
    Symptoms = db.Column(db.String(2000), nullable=False)
    Severity_Level = db.Column(db.String(50), nullable=False)
    Similar_Diseases = db.Column(db.String(2000), nullable=False)
    Treatment_Recommendations = db.Column(db.String(2000), nullable=True)

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
    Symptoms = db.Column(db.String(2000), nullable=False)
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
    try:
        db.session.execute(text("SELECT 1"))  # Wrap the query with text()
        print("Database connection OK")
    except Exception as e:
        print("Database connection ERROR:", e)

# Routes
@app.route("/")
def home():
    first_name = session.get('first_name', 'Guest')
    return render_template("index.html", first_name=first_name)

@app.route("/set_session", methods=["POST"])
def set_session():
    data = request.get_json()
    session['first_name'] = data.get('first_name')
    session['email'] = data.get('email')
    return jsonify({"success": True})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "admintest@gmail.com" and password == "@Admin1234":
            session['email'] = email
            session['first_name'] = "Admin"
            return redirect(url_for('admin_dashboard'))

        user = Users.query.filter_by(Email=email, Password=password).first()
        if user:
            login_user(user)  # Log in the user using Flask-Login
            session['email'] = user.Email
            session['first_name'] = user.First_Name
            if user.Role == "Admin":
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        flash("Invalid email or password", "error")
    return render_template("login_signUp.html")

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('home'))

@app.route("/upload_disease_data", methods=["POST"])
def upload_disease_data():
    if request.method == "POST":
        try:
            image_file = request.files["image-upload"]
            disease_name = request.form.get("disease-name")
            symptoms = request.form.get("symptoms")
            severity_level = request.form.get("severity-level")
            similar_diseases = request.form.get("similar-diseases")
            treatment_recommendations = request.form.get("treatment")

            if not image_file or image_file.filename == "":
                return jsonify({"success": False, "error": "No image uploaded"})

            if not disease_name or not symptoms or not severity_level or not treatment_recommendations:
                return jsonify({"success": False, "error": "Missing required fields"})

            # Save the uploaded image
            image_filename = image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

            # Create a new Diseases object
            new_disease = Diseases(
                Image_URL=image_filename,
                Disease_Name=disease_name,
                Symptoms=symptoms,
                Severity_Level=severity_level,
                Similar_Diseases=similar_diseases,
                Treatment_Recommendations=treatment_recommendations
            )

            db.session.add(new_disease)
            db.session.commit()

            return jsonify({"success": True, "message": "Disease data uploaded successfully"})

        except Exception as e:
            print(f"Error uploading disease data: {e}")
            return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Invalid request"})

@app.route("/disease_recognition", methods=["GET", "POST"])
def disease_recognition():
    print("Current Session:", session)
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

                # Get the current user
                user_email = session.get('email')
                user = Users.query.filter_by(Email=user_email).first()
                if user is None:
                    return jsonify({"success": False, "error": "User not found"})

                # Save the uploaded image to the Plant_Images table
                new_image = Plant_Images(
                    User_ID=user.User_ID,
                    Upload_Date=date.today(),
                    Image_URL=file.filename,
                    Quality_Status="Good"
                )
                db.session.add(new_image)
                db.session.commit()

                # Process the image for prediction
                image = Image.open(filepath)
                image = image.resize((128, 128))  # Resize image to match model input size
                input_arr = tf.keras.preprocessing.image.img_to_array(image)
                img_array = np.array([input_arr])

                # Prediction
                prediction = model.predict(img_array)
                confidence = np.max(prediction) * 100  # Get confidence score
                labels = [
                    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_rust', 'Apple___healthy',
                    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
                    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust',
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

                # Save the diagnosis result to the Diagnosis_Results table
                disease = Diseases.query.filter_by(Disease_Name=predicted_label).first()
                if not disease:
                    return jsonify({"success": False, "error": "Disease not found in database"})

                new_diagnosis = Diagnosis_Results(
                    Image_ID=new_image.Image_ID,
                    Disease_ID=disease.Disease_ID,
                    Predicted_Disease=predicted_label,
                    Percentage_Confidence=float(confidence),
                    Diagnosis_Method="AI Prediction",
                    Diagnosis_Date=date.today()
                )
                db.session.add(new_diagnosis)
                db.session.commit()

                # Return the prediction result and diagnosis ID for feedback
                return jsonify({
                    "success": True,
                    "prediction": predicted_label,
                    "confidence": float(confidence),
                    "image_url": file.filename,
                    "diagnosis_id": new_diagnosis.Result_ID  # Pass the diagnosis ID for feedback
                })
              
            except Exception as e:
                return jsonify({"success": False, "error": str(e)})

    return render_template("disease_recognition.html")

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    if request.method == "POST":
        try:
            # Get form data
            accuracy = request.form.get('accuracy')
            rating = request.form.get('rating')
            comments = request.form.get('comments')
            diagnosis_id = request.form.get('diagnosis_id')

            # Debugging: Print received data
            print(f"Received feedback data: accuracy={accuracy}, rating={rating}, comments={comments}, diagnosis_id={diagnosis_id}")

            # If diagnosis_id is missing or invalid, generate a random one
            if not diagnosis_id or not diagnosis_id.isdigit():
                diagnosis_id = random.randint(1, 99)  # Generate a random ID between 1 and 99
                print(f"Generated random diagnosis_id: {diagnosis_id}")

            # Convert diagnosis_id to integer
            diagnosis_id = int(diagnosis_id)

            # Get the current user ID
            if 'email' not in session:
                return jsonify({"success": False, "error": "User not authenticated"})

            user_email = session.get('email')
            user = Users.query.filter_by(Email=user_email).first()
            if not user:
                return jsonify({"success": False, "error": "User not found"})

            user_id = user.User_ID

            # Validate diagnosis ID (ensure it exists in the diagnosis_results table)
            diagnosis = Diagnosis_Results.query.get(diagnosis_id)
            if not diagnosis:
                # If the diagnosis ID does not exist, create a new dummy diagnosis
                new_diagnosis = Diagnosis_Results(
                    Image_ID=1,  # Use a valid Image_ID or create a dummy one
                    Disease_ID=1,  # Use a valid Disease_ID or create a dummy one
                    Predicted_Disease="Dummy Disease",
                    Percentage_Confidence=0.0,
                    Diagnosis_Method="Manual",
                    Diagnosis_Date=date.today()
                )
                db.session.add(new_diagnosis)
                db.session.commit()
                diagnosis_id = new_diagnosis.Result_ID  # Use the new diagnosis ID

            # Create a new feedback entry
            new_feedback = Feedback(
                User_ID=user_id,
                Diagnosis_ID=diagnosis_id,
                Feedback_Date=date.today(),
                Prediction_Accuracy=int(accuracy),
                System_Rating=int(rating),
                Feedback_Text=comments
            )

            # Add and commit to the database
            db.session.add(new_feedback)
            db.session.commit()

            return jsonify({"success": True, "message": "Feedback submitted successfully"})

        except Exception as e:
            db.session.rollback()
            print(f"Error submitting feedback: {e}")
            return jsonify({"success": False, "error": str(e)})

    return jsonify({"success": False, "error": "Invalid request"})

# Expert Consultation Page (Protected)
@app.route("/expert")
def expert():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template("expert.html")

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Serve static files (images, CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

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
            # SignUpdate=date.today(),
            Role=user_role,
            Phone_number=phone_number,
            Email=email,
            Password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid request"})

    
@app.route("/admin/dashboard_counts", methods=["GET"])
def get_dashboard_counts():
    try:
        # Fetch counts from the database
        total_users = Users.query.count()
        total_reports = Feedback.query.count()
        active_diagnoses = Diagnosis_Results.query.count()

        # Return the counts as JSON
        return jsonify({
            "total_users": total_users,
            "total_reports": total_reports,
            "active_diagnoses": active_diagnoses
        })
    except Exception as e:
        print(f"Error fetching dashboard counts: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route("/admin/feedback", methods=["GET"])
def get_feedback():
    try:
        # Fetch feedback data with user details
        feedback_data = db.session.query(
            Feedback, Users
        ).join(
            Users, Feedback.User_ID == Users.User_ID
        ).all()

        # Prepare the data to be returned as JSON
        feedback_list = [{
            "User_Name": f"{user.First_Name} {user.Last_Name}",  # Concatenate First_Name and Last_Name
            "Email": user.Email,
            "Feedback_Text": feedback.Feedback_Text
        } for feedback, user in feedback_data]

        return jsonify(feedback_list)  # Return the data as JSON
    except Exception as e:
        print(f"Error fetching feedback: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/save_treatment", methods=["POST"])
def save_treatment():
    try:
        # Get form data
        data = request.get_json()
        disease_name = data.get("disease_name")
        symptoms = data.get("symptoms")
        preventive_measures = data.get("preventive_measures")
        chemical_treatments = data.get("chemical_treatments")
        organic_solutions = data.get("organic_solutions")
        best_farming_practices = data.get("best_farming_practices")

        # Validate required fields
        if not disease_name or not symptoms or not preventive_measures or not chemical_treatments or not organic_solutions or not best_farming_practices:
            return jsonify({"success": False, "error": "All fields are required"})

        # Check if the disease already exists in the diseases table
        disease = Diseases.query.filter_by(Disease_Name=disease_name).first()
        if not disease:
            # If the disease doesn't exist, create a new entry in the diseases table
            disease = Diseases(
                Disease_Name=disease_name,
                Image_URL="/static/uploads/download.jpg",  # Provide a default image or handle image upload separately
                Symptoms=symptoms,
                Severity_Level="Unknown",  # Provide a default severity level
                Similar_Diseases="None",  # Provide a default value
                Treatment_Recommendations="None"  # Provide a default value
            )
            db.session.add(disease)
            db.session.commit()

        # Create a new Treatment_Recommendations object
        new_treatment = Treatment_Recommendations(
            Disease_ID=disease.Disease_ID,  # Use the Disease_ID from the diseases table
            Created_Date=date.today(),
            Disease_Name=disease_name,
            Symptoms=symptoms,
            Preventive_Measures=preventive_measures,
            Chemical_Treatments=chemical_treatments,
            Organic_Solutions=organic_solutions,
            Best_Farming_Practices=best_farming_practices
        )

        # Add and commit to the database
        db.session.add(new_treatment)
        db.session.commit()

        return jsonify({"success": True, "message": "Treatment data saved successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error saving treatment data: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

  
@app.route("/admin/get_diseases", methods=["GET"])
def get_diseases():
    try:
        diseases = Diseases.query.all()
        diseases_list = [{
            "Disease_ID": disease.Disease_ID,
            "Disease_Name": disease.Disease_Name,
            "Symptoms": disease.Symptoms,
            "Severity_Level": disease.Severity_Level,
            "Similar_Diseases": disease.Similar_Diseases,
            "Treatment_Recommendations": disease.Treatment_Recommendations
        } for disease in diseases]
        return jsonify({"success": True, "diseases": diseases_list})
    except Exception as e:
        print(f"Error fetching diseases: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/admin/get_treatment_recommendations/<disease_name>", methods=["GET"])
def get_treatment_recommendations(disease_name):
    try:
        # Fetch treatment recommendations for the given disease name
        treatment = Treatment_Recommendations.query.filter_by(Disease_Name=disease_name).first()
        if treatment:
            treatment_data = {
                "Preventive_Measures": treatment.Preventive_Measures,
                "Chemical_Treatments": treatment.Chemical_Treatments,
                "Organic_Solutions": treatment.Organic_Solutions,
                "Best_Farming_Practices": treatment.Best_Farming_Practices
            }
            return jsonify({"success": True, "treatment": treatment_data})
        else:
            return jsonify({"success": False, "error": "No treatment recommendations found for this disease"})
    except Exception as e:
        print(f"Error fetching treatment recommendations: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/update_user_role/<int:user_id>", methods=["POST"])
def update_user_role(user_id):
    if not is_logged_in() or session.get('first_name') != "Admin":
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        data = request.get_json()
        new_role = data.get('role')
        
        if not new_role:
            return jsonify({"success": False, "error": "Role is required"}), 400

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        user.Role = new_role
        db.session.commit()

        return jsonify({"success": True, "message": "User role updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user role: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route("/admin/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_logged_in() or session.get('first_name') != "Admin":
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    try:
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"success": False, "error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"success": True, "message": "User deleted successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/users", methods=["GET"])
def get_users():
    try:
        # Fetch all users from the database ordered by User_ID
        users = Users.query.order_by(Users.User_ID).all()
        
        # Prepare complete user data
        users_data = [{
            "User_ID": user.User_ID,
            "First_Name": user.First_Name,
            "Last_Name": user.Last_Name,
            "Email": user.Email,
            "Password": "********",  # Mask password for security
            "Role": user.Role,
            "Phone_number": user.Phone_number,
            "Full_Name": f"{user.First_Name} {user.Last_Name}"
        } for user in users]
        
        return jsonify(users_data)
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
#SYSTEM REPORTS:
# Add these new routes to your app.py
# Reports Routes (updated)
@app.route("/admin/reports/logged_users")
def get_logged_users_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Validate dates
        if not start_date or not end_date:
            return jsonify({"success": False, "error": "Start and end dates are required"}), 400

        # Query to get logged-in users count by date with date filtering
        result = db.session.query(
            func.date(Diagnosis_Results.Diagnosis_Date).label('date'),
            func.count(distinct(Diagnosis_Results.Image_ID)).label('user_count')
        ).filter(
            Diagnosis_Results.Diagnosis_Date >= start_date,
            Diagnosis_Results.Diagnosis_Date <= end_date
        ).group_by(
            func.date(Diagnosis_Results.Diagnosis_Date)
        ).order_by(
            func.date(Diagnosis_Results.Diagnosis_Date)
        ).all()

        # Format data for Chart.js
        dates = [str(row.date) for row in result]
        counts = [row.user_count for row in result]

        return jsonify({
            "success": True,
            "labels": dates,
            "data": counts
        })
    except Exception as e:
        print(f"Error fetching logged users report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/plant_diseases")
def get_plant_diseases_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Query to get disease frequency with date filtering
        result = db.session.query(
            Diseases.Disease_Name,
            func.count(Diagnosis_Results.Result_ID).label('count')
        ).join(
            Diagnosis_Results, Diagnosis_Results.Disease_ID == Diseases.Disease_ID
        ).filter(
            Diagnosis_Results.Diagnosis_Date >= start_date,
            Diagnosis_Results.Diagnosis_Date <= end_date
        ).group_by(
            Diseases.Disease_Name
        ).order_by(
            func.count(Diagnosis_Results.Result_ID).desc()
        ).all()

        # Format data for Chart.js
        diseases = [row.Disease_Name for row in result]
        counts = [row.count for row in result]

        return jsonify({
            "success": True,
            "labels": diseases,
            "data": counts
        })
    except Exception as e:
        print(f"Error fetching plant diseases report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/user_feedback")
def get_user_feedback_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Query to get all feedback with user details and date filtering
        feedback = db.session.query(
            Feedback,
            Users
        ).join(
            Users, Feedback.User_ID == Users.User_ID
        ).filter(
            Feedback.Feedback_Date >= start_date,
            Feedback.Feedback_Date <= end_date
        ).order_by(
            Feedback.Feedback_Date.desc()
        ).all()

        # Format data for table
        feedback_list = [{
            "user_name": f"{user.First_Name} {user.Last_Name}",
            "email": user.Email,
            "feedback": feedback.Feedback_Text,
            "rating": feedback.System_Rating,
            "date": str(feedback.Feedback_Date)
        } for feedback, user in feedback]

        return jsonify({
            "success": True,
            "feedback": feedback_list
        })
    except Exception as e:
        print(f"Error fetching user feedback report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/disease_trends")
def get_disease_trends_report():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Query to get disease trends over time with date filtering
        result = db.session.query(
            func.date(Diagnosis_Results.Diagnosis_Date).label('date'),
            Diseases.Disease_Name,
            func.count(Diagnosis_Results.Result_ID).label('count')
        ).join(
            Diseases, Diagnosis_Results.Disease_ID == Diseases.Disease_ID
        ).filter(
            Diagnosis_Results.Diagnosis_Date >= start_date,
            Diagnosis_Results.Diagnosis_Date <= end_date
        ).group_by(
            func.date(Diagnosis_Results.Diagnosis_Date),
            Diseases.Disease_Name
        ).order_by(
            func.date(Diagnosis_Results.Diagnosis_Date)
        ).all()

        # Format data for multi-line chart
        dates = sorted(list(set([str(row.date) for row in result])))
        diseases = list(set([row.Disease_Name for row in result]))
        
        datasets = []
        for disease in diseases:
            counts = []
            for date in dates:
                count = next((row.count for row in result if str(row.date) == date and row.Disease_Name == disease), 0)
                counts.append(count)
            
            datasets.append({
                "label": disease,
                "data": counts,
                "borderColor": f"#{random.randint(0, 0xFFFFFF):06x}",  # Random color
                "fill": False
            })

        return jsonify({
            "success": True,
            "labels": dates,
            "datasets": datasets
        })
    except Exception as e:
        print(f"Error fetching disease trends report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)