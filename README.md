# GunduziAI - AI-Driven Plant Disease Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

An intelligent plant disease detection platform leveraging Convolutional Neural Networks (CNNs) to empower Kenyan farmers with real-time crop health diagnostics and treatment recommendations.

## 🌱 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Model Details](#model-details)
- [API Documentation](#api-documentation)
- [Dataset](#dataset)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Contact](#contact)

## 🎯 Overview

GunduziAI addresses critical food security challenges in Kenya by providing smallholder farmers with accessible AI-powered plant disease detection. The system analyzes leaf images to identify diseases across multiple crops including tomatoes, maize, potatoes, and fruits, delivering instant diagnoses and evidence-based treatment recommendations.

<img width="1600" height="900" alt="Screenshot (415)" src="https://github.com/user-attachments/assets/a9ac6e59-ab35-4d1a-b708-c1ad8c73f5e7" />


### Vision
To revolutionize agricultural practices in East Africa through accessible AI technology, reducing crop losses and improving farmer livelihoods.

### Mission
Empower farmers with real-time disease detection, connect them with agricultural experts, and build comprehensive disease surveillance data for research and policy development.

## ✨ Key Features

### 🌿 Core Capabilities
- **Real-Time Disease Detection**: Instant analysis of plant leaf images using advanced CNN models
- **Multi-Crop Support**: Comprehensive coverage for 38 plant disease categories
- **Treatment Recommendations**: Evidence-based solutions for identified diseases
- **Expert Validation System**: Agronomist review for uncertain diagnoses
- **Disease Trend Analytics**: Anonymized data for agricultural research
- **Multi-Platform Access**: Web and mobile-friendly interfaces

### 🔬 Technical Features
- **High-Accuracy CNN Models**: Trained on diverse plant disease datasets
- **Scalable Architecture**: Cloud-ready with PostgreSQL and Firebase
- **RESTful API**: Clean interfaces for third-party integrations
- **Data Privacy**: Secure handling of farmer and image data
- **Offline Capability**: Planned mobile support for low-connectivity areas

## 🏗️ System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   AI Model      │
│   (Web/Mobile)  │◄──►│   (Flask)        │◄──►│   (TensorFlow)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Firebase       │    │   File Storage  │
│   (User Data)   │    │   (Auth/Storage) │    │   (Images)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack
- **Backend**: Python, Flask, TensorFlow 2.10+
- **Database**: PostgreSQL 14+
- **Authentication**: Firebase Auth
- **Storage**: Firebase Storage + Local File System
- **Computer Vision**: OpenCV, Pillow
- **Model Training**: TensorFlow/Keras, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap

## 🚀 Installation

### Prerequisites

#### System Requirements
- **Python**: 3.8 or higher
- **PostgreSQL**: 14 or higher
- **RAM**: 8GB minimum (16GB recommended for training)
- **Storage**: 10GB free space
- **GPU**: Optional but recommended for model training (NVIDIA CUDA-compatible)

#### Required Python Packages
```txt
tensorflow>=2.10.0
flask>=2.0.0
opencv-python>=4.5.0
pillow>=8.3.0
numpy>=1.21.0
pandas>=1.3.0
sqlalchemy>=1.4.0
psycopg2-binary>=2.9.0
firebase-admin>=5.0.0
gunicorn>=20.0.0
```

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/VincentOracle/GunduziAI-AI-DRIVEN-PLANT-DISEASE-DETECTION-SYSTEM.git
cd GunduziAI-AI-DRIVEN-PLANT-DISEASE-DETECTION-SYSTEM
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv gunduzi_env
gunduzi_env\Scripts\activate

# Linux/Mac
python3 -m venv gunduzi_env
source gunduzi_env/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Database Setup

**PostgreSQL Configuration:**
```sql
CREATE DATABASE gunduziai;
CREATE USER gunduzi_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE gunduziai TO gunduzi_user;
```

**Update Configuration:**
Create `config.py`:
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://gunduzi_user:your_secure_password@localhost/gunduziai'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Firebase Configuration
    FIREBASE_CREDENTIALS = 'path/to/your/firebase-adminsdk.json'
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
```

#### 5. Firebase Setup
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Download service account key as `firebase-adminsdk.json`
3. Place in project root directory

#### 6. Initialize Database
```bash
python init_db.py
```

## 🎯 Quick Start

### Running the Application

#### Development Mode
```bash
# Activate virtual environment
source gunduzi_env/bin/activate  # Linux/Mac
# OR
gunduzi_env\Scripts\activate    # Windows

# Run Flask application
python app.py
```

#### Production Mode
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Access the Application
- **Web Interface**: http://localhost:5000
- **API Base URL**: http://localhost:5000/api

### Demo Access
- Pre-trained models are available in `/models` directory
- Sample test images in `/data/samples`
- Default test credentials (if implemented)


<img width="1600" height="900" alt="Screenshot (404)" src="https://github.com/user-attachments/assets/411aab8a-878c-4edf-881b-53575b160171" />

## 🧠 Model Details

### Supported Plant Diseases
The system detects 38 different plant health conditions across multiple crops:

```python
DISEASE_LABELS = [
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
```

### CNN Architecture
- **Base Model**: Custom CNN or Transfer Learning (EfficientNet/MobileNet)
- **Input Size**: 224x224 pixels RGB
- **Output**: 38-class softmax classification
- **Accuracy**: >90% on test dataset
- **Inference Time**: <2 seconds per image

### Model Training
```python
# Example training configuration
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_generator,
    epochs=50,
    validation_data=val_generator,
    callbacks=[early_stopping, model_checkpoint]
)
```

## 📚 API Documentation

### Endpoints

#### 1. Health Check
```http
GET /api/health
```
**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Disease Detection
```http
POST /api/detect
Content-Type: multipart/form-data
```
**Parameters:**
- `image`: Plant leaf image file (jpg, png, jpeg)
- `crop_type`: Optional crop type for improved accuracy

**Response:**
```json
{
    "disease": "Tomato___Early_blight",
    "confidence": 0.934,
    "treatment": "Apply copper-based fungicides...",
    "prevention": "Ensure proper spacing...",
    "confidence_level": "high"
}
```

#### 3. Expert Consultation Request
```http
POST /api/consult
Content-Type: application/json
```
**Body:**
```json
{
    "image_id": "img_12345",
    "farmer_notes": "Noticed yellow spots last week",
    "contact_method": "sms"
}
```

#### 4. Disease Trends
```http
GET /api/trends?region=Central&crop=Tomato&period=30d
```
**Response:**
```json
{
    "trends": [
        {
            "disease": "Late_blight",
            "count": 45,
            "increase": 15
        }
    ],
    "regional_data": {...}
}
```

## 📊 Dataset

### Training Data
- **Source**: PlantVillage dataset + Local Kenyan farm data
- **Total Images**: 50,000+ labeled images
- **Classes**: 38 plant disease categories
- **Augmentation**: Rotation, flipping, brightness adjustment

### Data Preprocessing Pipeline
```python
def preprocess_image(image_path):
    # Load and resize image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    
    # Normalize pixel values
    image = image / 255.0
    
    # Data augmentation (training only)
    if training:
        image = apply_augmentation(image)
    
    return image
```

## 🌍 Deployment

### Production Deployment Options

#### 1. Cloud Deployment (Recommended)
```bash
# Using Docker
docker build -t gunduziai .
docker run -p 5000:5000 gunduziai

# Using cloud platforms
# - AWS Elastic Beanstalk
# - Google Cloud Run
# - Azure Container Instances
```

#### 2. Local Server Deployment
```bash
# Install and configure nginx
sudo apt install nginx
sudo systemctl enable nginx

# Configure reverse proxy
# /etc/nginx/sites-available/gunduziai
```

### Environment Variables
```bash
export SECRET_KEY='your-production-secret-key'
export DATABASE_URL='postgresql://user:pass@host:5432/gunduziai'
export FIREBASE_CREDENTIALS='path/to/firebase.json'
export MODEL_PATH='models/plant_disease_model.h5'
```

## 🔧 Development

### Project Structure
```
GunduziAI/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── models/               # Trained ML models
│   └── plant_disease_model.h5
├── static/               # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── results.html
├── utils/                # Utility functions
│   ├── model_loader.py
│   ├── image_processor.py
│   └── disease_info.py
├── database/             # Database models and operations
│   ├── models.py
│   └── operations.py
└── tests/                # Test suite
    ├── test_api.py
    ├── test_model.py
    └── test_integration.py
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/ -v
```

### Code Contribution
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request

## 🎓 Academic Information

### Project Details
- **System Title**: AI-Driven Plant Disease Detection System
- **Developer**: Were Vincent Ouma
- **Registration Number**: J17/MNU/7428/2020
- **Supervisor**: Dr. Michael Munyao
- **Academic Year**: 2024/2025
- **Institution**: Kenyatta University

### Research Impact
- **Food Security**: Reducing crop losses for smallholder farmers
- **Technology Access**: Bridging digital divide in rural agriculture
- **Data Analytics**: Building comprehensive disease surveillance system
- **Climate Resilience**: Supporting adaptation to climate change

## 🔮 Future Roadmap

### Short-term Goals (2024)
- [ ] Mobile application development
- [ ] Swahili language interface
- [ ] SMS-based query system
- [ ] Expanded crop coverage

### Medium-term Goals (2025)
- [ ] IoT sensor integration
- [ ] Offline mobile capability
- [ ] Regional adaptation models
- [ ] Farmer training modules

### Long-term Vision (2026+)
- [ ] Pan-African deployment
- [ ] Predictive outbreak modeling
- [ ] Blockchain for supply chain
- [ ] Climate impact analysis

## 🤝 Contributing

We welcome contributions from developers, researchers, and agricultural experts:

1. **Bug Reports**: Use GitHub Issues with detailed descriptions
2. **Feature Requests**: Suggest new capabilities or improvements
3. **Code Contributions**: Follow PEP8 standards and include tests
4. **Documentation**: Help improve guides and translations
5. **Testing**: Test on different devices and network conditions

### Development Setup
```bash
# Fork and clone
git clone https://github.com/your-username/GunduziAI.git
cd GunduziAI

# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

## 📞 Contact & Support

### Primary Developer
**Were Vincent Ouma**
- 📧 Email: [oumawere2001@gmail.com](mailto:oumawere2001@gmail.com)
- 📱 Phone: +254 768653509
- 🏫 Institution: Kenyatta University
- 🎓 Department: Computing and Information Science
- 🔗 GitHub: [VincentOracle](https://github.com/VincentOracle)

### Repository
```bash
git clone https://github.com/VincentOracle/GunduziAI-AI-DRIVEN-PLANT-DISEASE-DETECTION-SYSTEM.git
```

### Support Channels
- **Documentation**: Project README and wiki
- **Issues**: GitHub Issues tracker
- **Email**: Direct developer contact for critical issues
- **Community**: Future farmer support forums planned

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kenyatta University** for academic guidance and support
- **Dr. Michael Munyao** for supervision and mentorship
- **PlantVillage** for open-source disease dataset
- **Kenyan Farmers** for field testing and feedback
- **Open Source Community** for tools and libraries

---

**GunduziAI** - *Illuminating the path to healthier crops and sustainable agriculture in Kenya.*

*Last Updated: January 2024*  
*Project Status: Complete Development*

# USER INTERFACES AND DASHBORADS

<img width="1600" height="900" alt="Screenshot (417)" src="https://github.com/user-attachments/assets/78792ed5-2363-4b21-9098-4476273e7192" />
<img width="1600" height="900" alt="Screenshot (416)" src="https://github.com/user-attachments/assets/e0161eb3-d323-4691-9809-e8dd17508037" />
<img width="1600" height="900" alt="Screenshot (415)" src="https://github.com/user-attachments/assets/96b08084-2266-46cd-9352-88352c2766be" />
<img width="1600" height="900" alt="Screenshot (413)" src="https://github.com/user-attachments/assets/0234176f-b1ce-4185-b0e6-62f50abfcd12" />
<img width="1600" height="900" alt="Screenshot (412)" src="https://github.com/user-attachments/assets/fe3a14c2-1a69-43b2-9b57-470f9e4ba3b6" />
<img width="1600" height="900" alt="Screenshot (404)" src="https://github.com/user-attachments/assets/58e98e87-5042-47fa-8df2-42fad47f92df" />
<img width="1600" height="900" alt="Screenshot (403)" src="https://github.com/user-attachments/assets/cb472692-2bfa-45df-8a9c-9c14474ba65f" />
<img width="1600" height="900" alt="Screenshot (431)" src="https://github.com/user-attachments/assets/f6aa1222-9cf3-489d-9c32-05f72a4f3af1" />
<img width="1600" height="900" alt="Screenshot (419)" src="https://github.com/user-attachments/assets/f907fd43-00c3-4ce8-9016-0250ed1d1875" />
<img width="1600" height="900" alt="Screenshot (418)" src="https://github.com/user-attachments/assets/3e95fbd6-fdb3-4cdd-909f-d6425312b7cb" />

