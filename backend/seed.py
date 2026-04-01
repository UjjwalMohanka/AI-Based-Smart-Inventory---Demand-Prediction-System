"""
Seed database with realistic inventory and sales data
"""
import sys
from datetime import datetime, timedelta
import numpy as np
from app import create_app
from models import db, User, Product, Inventory, Sales

def generate_seasonal_sales(base_qty, months=18):
    """
    Generate realistic sales data with trend and seasonality
    
    Args:
        base_qty: Base quantity per month
        months: Number of months to generate
        
    Returns:
        List of monthly quantities
    """
    sales = []
    
    for month in range(months):
        # Trend component (gradual increase)
        trend = base_qty * (1 + 0.02 * month)
        
        # Seasonal component (peaks in March and October)
        seasonal = np.sin(2 * np.pi * month / 12) * 0.15 * base_qty
        
        # Add random noise (±15%)
        noise = np.random.uniform(-0.15, 0.15) * base_qty
        
        # Combine components
        quantity = max(0, int(trend + seasonal + noise))
        sales.append(quantity)
    
    return sales


def seed_database():
    """Seed the database with realistic data"""
    
    print("\n🌱 Seeding database...\n")
    
    # Clear existing data
    db.drop_all()
    db.create_all()
    print("✓ Database tables created")
    
    # Create admin user
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create viewer user
    viewer = User(username='viewer', role='viewer')
    viewer.set_password('viewer123')
    db.session.add(viewer)
    
    print("✓ Created users: admin/admin123, viewer/viewer123")
    
    # Product data
    products_data = [
        {
            'name': 'Steel Rods',
            'category': 'Metal',
            'unit': 'kg',
            'reorder_point': 300,
            'lead_time_days': 10,
            'base_sales': 350,
            'initial_stock': 500
        },
        {
            'name': 'Copper Wire',
            'category': 'Metal',
            'unit': 'meters',
            'reorder_point': 500,
            'lead_time_days': 7,
            'base_sales': 600,
            'initial_stock': 800
        },
        {
            'name': 'PVC Pipes',
            'category': 'Plastic',
            'unit': 'units',
            'reorder_point': 200,
            'lead_time_days': 5,
            'base_sales': 250,
            'initial_stock': 350
        },
        {
            'name': 'Aluminum Sheets',
            'category': 'Metal',
            'unit': 'sheets',
            'reorder_point': 150,
            'lead_time_days': 14,
            'base_sales': 180,
            'initial_stock': 250
        },
        {
            'name': 'Rubber Gaskets',
            'category': 'Rubber',
            'unit': 'units',
            'reorder_point': 400,
            'lead_time_days': 7,
            'base_sales': 450,
            'initial_stock': 600
        },
        {
            'name': 'Industrial Bolts',
            'category': 'Hardware',
            'unit': 'boxes',
            'reorder_point': 100,
            'lead_time_days': 3,
            'base_sales': 120,
            'initial_stock': 180
        },
        {
            'name': 'Paint Drums',
            'category': 'Chemical',
            'unit': 'drums',
            'reorder_point': 50,
            'lead_time_days': 10,
            'base_sales': 60,
            'initial_stock': 90
        },
        {
            'name': 'Circuit Boards',
            'category': 'Electronics',
            'unit': 'units',
            'reorder_point': 80,
            'lead_time_days': 21,
            'base_sales': 100,
            'initial_stock': 120
        }
    ]
    
    # Create products and generate sales history
    warehouse_locations = ['Warehouse A', 'Warehouse B', 'Warehouse C']
    
    # Starting date (18 months ago)
    start_date = datetime.now() - timedelta(days=18*30)
    
    for idx, product_data in enumerate(products_data):
        # Create product
        product = Product(
            name=product_data['name'],
            category=product_data['category'],
            unit=product_data['unit'],
            reorder_point=product_data['reorder_point'],
            lead_time_days=product_data['lead_time_days']
        )
        db.session.add(product)
        db.session.flush()  # Get product ID
        
        # Create inventory
        inventory = Inventory(
            product_id=product.id,
            quantity_in_stock=product_data['initial_stock'],
            warehouse_location=warehouse_locations[idx % 3]
        )
        db.session.add(inventory)
        
        # Generate 18 months of sales data
        monthly_sales = generate_seasonal_sales(product_data['base_sales'], months=18)
        
        for month_offset, quantity in enumerate(monthly_sales):
            sale_date = start_date + timedelta(days=month_offset * 30)
            
            sale = Sales(
                product_id=product.id,
                quantity_sold=quantity,
                sale_date=sale_date.date(),
                month=sale_date.month,
                year=sale_date.year
            )
            db.session.add(sale)
        
        print(f"✓ Created product: {product.name} with 18 months of sales data")
    
    # Commit all changes
    db.session.commit()
    
    print(f"\n✅ Database seeded successfully!")
    print(f"   - {len(products_data)} products created")
    print(f"   - {len(products_data) * 18} sales records generated")
    print(f"   - 2 users created\n")


if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        try:
            seed_database()
        except Exception as e:
            print(f"\n❌ Error seeding database: {str(e)}")
            sys.exit(1)
