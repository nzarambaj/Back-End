import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use PostgreSQL in production, SQLite for local development
    if os.getenv("VERCEL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", "sqlite:///imagingsystem.db")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
    DICOM_STORAGE_PATH = os.getenv("DICOM_STORAGE_PATH", "/tmp/dicom_storage")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    DICOM_STORAGE_PATH = os.getenv("DICOM_STORAGE_PATH", "/tmp/dicom_storage")