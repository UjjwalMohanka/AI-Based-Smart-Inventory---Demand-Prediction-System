from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from models import db, Sales, Product
from sqlalchemy import func

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@sales_bp.route('', methods=['POST'])
@jwt_required()
def create_sale():
    """Log a new sale"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'product_id' not in data or 'quantity_sold' not in data:
            return jsonify({'error': 'product_id and quantity_sold required'}), 400
        
        # Check if product exists
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Parse sale date
        if 'sale_date' in data:
            sale_date = datetime.fromisoformat(data['sale_date'].replace('Z', '+00:00')).date()
        else:
            sale_date = datetime.utcnow().date()
        
        # Create sale record
        sale = Sales(
            product_id=data['product_id'],
            quantity_sold=data['quantity_sold'],
            sale_date=sale_date,
            month=sale_date.month,
            year=sale_date.year
        )
        
        db.session.add(sale)
        db.session.commit()
        
        return jsonify({
            'message': 'Sale recorded successfully',
            'sale': sale.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_sales(product_id):
    """Get sales history for a specific product"""
    try:
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get sales ordered by date
        sales = Sales.query.filter_by(product_id=product_id).order_by(
            Sales.year.desc(), Sales.month.desc(), Sales.sale_date.desc()
        ).all()
        
        return jsonify([sale.to_dict() for sale in sales]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sales_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_sales_summary():
    """Get monthly sales summary for all products"""
    try:
        # Aggregate sales by product and month
        summary = db.session.query(
            Sales.product_id,
            Product.name,
            Sales.year,
            Sales.month,
            func.sum(Sales.quantity_sold).label('total_sold')
        ).join(Product).group_by(
            Sales.product_id, Product.name, Sales.year, Sales.month
        ).order_by(
            Sales.year.desc(), Sales.month.desc()
        ).all()
        
        # Format results
        results = []
        for row in summary:
            results.append({
                'product_id': row.product_id,
                'product_name': row.name,
                'year': row.year,
                'month': row.month,
                'total_sold': row.total_sold
            })
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sales_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent_sales():
    """Get recent sales (last 50)"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        sales = Sales.query.order_by(
            Sales.created_at.desc()
        ).limit(limit).all()
        
        return jsonify([sale.to_dict() for sale in sales]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
