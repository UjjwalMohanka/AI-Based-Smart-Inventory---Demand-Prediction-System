from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product, Inventory, Sales, Prediction
from ml.predictor import predict_demand, calculate_restock_suggestion

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predict')

@prediction_bp.route('', methods=['POST'])
@jwt_required()
def generate_prediction():
    """
    Generate demand prediction for a product
    
    Request body:
        {
            "product_id": int,
            "months_ahead": int (default: 3, max: 12)
        }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'product_id' not in data:
            return jsonify({'error': 'product_id required'}), 400
        
        product_id = data['product_id']
        months_ahead = min(data.get('months_ahead', 3), 12)  # Cap at 12 months
        
        # Get product
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get sales history
        sales_records = Sales.query.filter_by(product_id=product_id).order_by(
            Sales.year, Sales.month
        ).all()
        
        if not sales_records:
            return jsonify({
                'error': 'No sales history available for this product',
                'product_name': product.name
            }), 400
        
        # Generate predictions
        prediction_result = predict_demand(sales_records, months_ahead)
        
        # Get current inventory
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        current_stock = inventory.quantity_in_stock if inventory else 0
        
        # Calculate restock suggestion
        restock_info = calculate_restock_suggestion(
            prediction_result['predictions'],
            current_stock,
            product.reorder_point,
            product.lead_time_days
        )
        
        # Save predictions to database
        for pred in prediction_result['predictions']:
            # Check if prediction already exists for this month/year
            existing = Prediction.query.filter_by(
                product_id=product_id,
                prediction_month=pred['month'],
                prediction_year=pred['year']
            ).first()
            
            if existing:
                # Update existing prediction
                existing.predicted_quantity = pred['predicted_qty']
                existing.confidence_score = prediction_result['accuracy']
            else:
                # Create new prediction
                new_pred = Prediction(
                    product_id=product_id,
                    predicted_quantity=pred['predicted_qty'],
                    prediction_month=pred['month'],
                    prediction_year=pred['year'],
                    confidence_score=prediction_result['accuracy']
                )
                db.session.add(new_pred)
        
        db.session.commit()
        
        # Format response
        response = {
            'product_id': product_id,
            'product_name': product.name,
            'predictions': prediction_result['predictions'],
            'current_stock': current_stock,
            'reorder_point': product.reorder_point,
            'restock_needed': restock_info['restock_needed'],
            'suggested_order_qty': restock_info['suggested_order_qty'],
            'restock_reason': restock_info['reason'],
            'accuracy_score': round(prediction_result['accuracy'], 3),
            'mae': round(prediction_result.get('mae', 0), 2),
            'model_type': prediction_result['model_type']
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@prediction_bp.route('/history/<int:product_id>', methods=['GET'])
@jwt_required()
def get_prediction_history(product_id):
    """Get prediction history for a product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        predictions = Prediction.query.filter_by(product_id=product_id).order_by(
            Prediction.prediction_year.desc(),
            Prediction.prediction_month.desc()
        ).all()
        
        return jsonify([pred.to_dict() for pred in predictions]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
