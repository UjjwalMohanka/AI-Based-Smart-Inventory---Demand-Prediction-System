from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Inventory, Product

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

@inventory_bp.route('', methods=['GET'])
@jwt_required()
def get_inventory():
    """Get all inventory items with product details"""
    try:
        inventory_items = Inventory.query.all()
        return jsonify([item.to_dict() for item in inventory_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@inventory_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_inventory_by_product(product_id):
    """Get inventory for a specific product"""
    try:
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        if not inventory:
            return jsonify({'error': 'Inventory not found for this product'}), 404
        
        return jsonify(inventory.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@inventory_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_inventory(product_id):
    """Update inventory quantity for a product"""
    try:
        data = request.get_json()
        
        # Validate input
        if 'quantity_in_stock' not in data:
            return jsonify({'error': 'quantity_in_stock required'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get or create inventory record
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        
        if not inventory:
            # Create new inventory record
            inventory = Inventory(
                product_id=product_id,
                quantity_in_stock=data['quantity_in_stock'],
                warehouse_location=data.get('warehouse_location')
            )
            db.session.add(inventory)
        else:
            # Update existing record
            inventory.quantity_in_stock = data['quantity_in_stock']
            if 'warehouse_location' in data:
                inventory.warehouse_location = data['warehouse_location']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Inventory updated successfully',
            'inventory': inventory.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@inventory_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get all products with low stock (below reorder point)"""
    try:
        # Query inventory items where stock < reorder_point
        low_stock_items = db.session.query(Inventory).join(Product).filter(
            Inventory.quantity_in_stock < Product.reorder_point
        ).all()
        
        return jsonify([item.to_dict() for item in low_stock_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
