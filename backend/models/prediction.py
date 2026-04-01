from datetime import datetime
from . import db

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    predicted_quantity = db.Column(db.Float, nullable=False)
    prediction_month = db.Column(db.Integer, nullable=False)  # 1-12
    prediction_year = db.Column(db.Integer, nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)  # R² score
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'predicted_quantity': round(self.predicted_quantity, 2),
            'prediction_month': self.prediction_month,
            'prediction_year': self.prediction_year,
            'confidence_score': round(self.confidence_score, 3) if self.confidence_score else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Prediction product_id={self.product_id} {self.prediction_year}-{self.prediction_month} qty={self.predicted_quantity}>'
