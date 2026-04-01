import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'smart-inventory-secret-key-123')
    FLASK_APP = 'run.py'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # MySQL Database - using mysqlconnector or pymysql
    # Basic format: mysql+pymysql://username:password@host:port/database
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'smart_inventory')
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'production.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT & Security
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-123')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Portfolio-Ready Settings
    SYSTEM_TITLE = "AI Smart Inventory & Demand AI"
    COMPANY_NAME = "Ujjwal's Industrial Solutions"
