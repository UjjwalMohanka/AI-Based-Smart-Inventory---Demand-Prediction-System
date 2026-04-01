from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User authentication model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    """Product details model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(50), nullable=False, default='units')
    reorder_point = db.Column(db.Integer, nullable=False, default=100)
    lead_time_days = db.Column(db.Integer, nullable=False, default=7)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='product', lazy=True, cascade='all, delete-orphan')
    sales = db.relationship('Sales', backref='product', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='product', lazy=True, cascade='all, delete-orphan')

class Inventory(db.Model):
    """Real-time inventory levels"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), unique=True, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)
    warehouse_location = db.Column(db.String(100), default='Main Warehouse')
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sales(db.Model):
    """Historical sales data for training"""
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.Date, nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    """AI-generated demand predictions"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    predicted_quantity = db.Column(db.Float, nullable=False)
    prediction_month = db.Column(db.Integer, nullable=False)
    prediction_year = db.Column(db.Integer, nullable=False)
    confidence_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
