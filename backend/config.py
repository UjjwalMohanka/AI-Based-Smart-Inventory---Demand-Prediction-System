import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretkey123')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Anthropic API
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'flask-secret-key-123')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
