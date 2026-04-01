import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.inventory import inventory_bp
    from routes.sales import sales_bp
    from routes.prediction import prediction_bp
    from routes.ai_chat import ai_chat_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(ai_chat_bp)
    app.register_blueprint(dashboard_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created")
    
    return app


if __name__ == '__main__':
    app = create_app()
    print(f"\n🚀 Smart Inventory API running on http://localhost:{Config.PORT}")
    print(f"📊 Database: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"🔐 JWT Auth enabled\n")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
