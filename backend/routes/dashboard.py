from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product, Inventory, Prediction
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """
    Get dashboard KPI statistics
    
    Returns:
        {
            "total_products": int,
            "low_stock_alerts": int,
            "total_stock_value": int,
            "prediction_accuracy_avg": float,
            "top_predicted_demand": {
                "product_id": int,
                "product_name": str,
                "predicted_qty": float
            }
        }
    """
    try:
        # Total products
        total_products = Product.query.count()
        
        # Low stock alerts (stock < reorder_point)
        low_stock_count = db.session.query(Inventory).join(Product).filter(
            Inventory.quantity_in_stock < Product.reorder_point
        ).count()
        
        # Total stock value (sum of all quantities)
        total_stock = db.session.query(
            func.sum(Inventory.quantity_in_stock)
        ).scalar() or 0
        
        # Average prediction accuracy (R² scores)
        avg_accuracy = db.session.query(
            func.avg(Prediction.confidence_score)
        ).filter(
            Prediction.confidence_score.isnot(None)
        ).scalar() or 0.0
        
        # Top predicted demand product (highest upcoming predicted quantity)
        top_prediction = db.session.query(
            Prediction.product_id,
            Product.name,
            func.sum(Prediction.predicted_quantity).label('total_predicted')
        ).join(Product).filter(
            Prediction.prediction_year >= db.func.strftime('%Y', db.func.date('now'))
        ).group_by(
            Prediction.product_id, Product.name
        ).order_by(
            func.sum(Prediction.predicted_quantity).desc()
        ).first()
        
        top_demand = None
        if top_prediction:
            top_demand = {
                'product_id': top_prediction.product_id,
                'product_name': top_prediction.name,
                'predicted_qty': round(top_prediction.total_predicted, 2)
            }
        
        # Get low stock items details
        low_stock_items = db.session.query(Inventory).join(Product).filter(
            Inventory.quantity_in_stock < Product.reorder_point
        ).all()
        
        low_stock_details = [item.to_dict() for item in low_stock_items]
        
        return jsonify({
            'total_products': total_products,
            'low_stock_alerts': low_stock_count,
            'total_stock_value': int(total_stock),
            'prediction_accuracy_avg': round(avg_accuracy, 3),
            'top_predicted_demand': top_demand,
            'low_stock_items': low_stock_details
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
