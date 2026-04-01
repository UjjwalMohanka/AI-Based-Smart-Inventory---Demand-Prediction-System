from datetime import datetime
from . import db

class Product(db.Model):
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
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'unit': self.unit,
            'reorder_point': self.reorder_point,
            'lead_time_days': self.lead_time_days,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'
