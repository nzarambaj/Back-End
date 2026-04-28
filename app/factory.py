from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from .database import db
from .config import Config

# route imports
from .routes.auth_routes import auth_bp
from .routes.mwl_routes import mwl_bp
from .routes.dicom_routes import dicom_bp
from .routes.settings_routes import settings_bp
from .routes.api_routes import api_bp
from .routes.root_routes import root_bp
from .routes.api_v2 import api_v2_bp
from .routes.medical_staff_routes import medical_staff_bp

# model imports
from .models.doctor import Doctor
from .models.patient_new import PatientNew
from .models.study import MRIStudy
from .models.image import MRIImage
from .models.medical_staff import MedicalStaff, Radiologist, ReferringDoctor, ImagingTechnician


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    jwt = JWTManager(app)
    
    # Configure JWT to handle string identity
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    
    db.init_app(app)

    # Don't create tables automatically in serverless environment
    # Tables should be created manually via init_db.py or migrations
    if not os.getenv("VERCEL"):
        with app.app_context():
            db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(mwl_bp)
    app.register_blueprint(dicom_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(root_bp)
    app.register_blueprint(api_v2_bp)
    app.register_blueprint(medical_staff_bp)

    return app