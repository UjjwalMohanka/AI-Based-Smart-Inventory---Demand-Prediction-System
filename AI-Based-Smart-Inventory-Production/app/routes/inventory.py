from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import db, Product, Inventory, Sales, Prediction
from ..utils.ml_engine import train_and_predict
from sqlalchemy import func
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def dashboard():
    """Main dashboard with KPIs and Charts"""
    total_products = Product.query.count()
    total_stock = db.session.query(func.sum(Inventory.quantity_in_stock)).scalar() or 0
    
    # Low stock alerts
    low_stock_items = db.session.query(Inventory).join(Product).filter(
        Inventory.quantity_in_stock <= Product.reorder_point
    ).all()
    
    # Recent predictions
    recent_predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                           total_products=total_products, 
                           total_stock=total_stock, 
                           low_stock_count=len(low_stock_items),
                           low_stock_items=low_stock_items,
                           recent_predictions=recent_predictions)

@inventory_bp.route('/inventory')
@login_required
def inventory_list():
    """List all products and their current stock"""
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@inventory_bp.route('/product/add', methods=['POST'])
@login_required
def add_product():
    """API/Route to add a new product"""
    name = request.form.get('name')
    category = request.form.get('category')
    unit = request.form.get('unit')
    reorder_point = int(request.form.get('reorder_point', 100))
    initial_stock = int(request.form.get('initial_stock', 0))
    
    product = Product(name=name, category=category, unit=unit, reorder_point=reorder_point)
    db.session.add(product)
    db.session.flush() # Get product ID
    
    inventory = Inventory(product_id=product.id, quantity_in_stock=initial_stock)
    db.session.add(inventory)
    db.session.commit()
    
    flash(f"Product '{name}' added successfully!", "success")
    return redirect(url_for('inventory.inventory_list'))

@inventory_bp.route('/predict/<int:product_id>')
@login_required
def predict(product_id):
    """Generate and store predictions for a product"""
    product = Product.query.get_or_404(product_id)
    historical_sales = Sales.query.filter_by(product_id=product_id).order_by(Sales.year, Sales.month).all()
    
    if not historical_sales:
        flash(f"No historical sales data for {product.name}. Cannot predict.", "warning")
        return redirect(url_for('inventory.inventory_list'))
        
    result = train_and_predict(historical_sales)
    
    # Clear old predictions for this product
    Prediction.query.filter_by(product_id=product_id).delete()
    
    # Store new predictions
    for p in result['predictions']:
        pred = Prediction(
            product_id=product_id,
            predicted_quantity=p['qty'],
            prediction_month=p['month'],
            prediction_year=p['year'],
            confidence_score=result['accuracy']
        )
        db.session.add(pred)
    
    db.session.commit()
    
    flash(f"Demand predictions generated for {product.name} (Accuracy: {result['accuracy']*100}%).", "info")
    return redirect(url_for('inventory.view_prediction', product_id=product_id))

@inventory_bp.route('/view_prediction/<int:product_id>')
@login_required
def view_prediction(product_id):
    """View detailed prediction graph for a product"""
    product = Product.query.get_or_404(product_id)
    historical_sales = Sales.query.filter_by(product_id=product_id).all()
    predictions = Prediction.query.filter_by(product_id=product_id).all()
    
    # Format data for Chart.js
    history_data = [{'month': s.month, 'year': s.year, 'qty': s.quantity_sold} for s in historical_sales]
    pred_data = [
        {
            'month': p.prediction_month, 
            'year': p.prediction_year, 
            'qty': p.predicted_quantity,
            'confidence_score': p.confidence_score
        } for p in predictions
    ]
    
    return render_template('prediction_detail.html', 
                           product=product, 
                           history=history_data, 
                           predictions=pred_data)
