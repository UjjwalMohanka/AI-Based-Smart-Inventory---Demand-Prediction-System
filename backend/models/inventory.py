from datetime import datetime
from . import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True, index=True)
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    warehouse_location = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """Convert inventory to dictionary with product info"""
        product = self.product
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': product.name if product else None,
            'category': product.category if product else None,
            'quantity_in_stock': self.quantity_in_stock,
            'reorder_point': product.reorder_point if product else None,
            'warehouse_location': self.warehouse_location,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'stock_status': self._get_stock_status()
        }
    
    def _get_stock_status(self):
        """Determine stock status (low, warning, good)"""
        if not self.product:
            return 'unknown'
        
        if self.quantity_in_stock < self.product.reorder_point:
            return 'low'
        elif self.quantity_in_stock < (self.product.reorder_point * 2):
            return 'warning'
        else:
            return 'good'
    
    def __repr__(self):
        return f'<Inventory product_id={self.product_id} stock={self.quantity_in_stock}>'
