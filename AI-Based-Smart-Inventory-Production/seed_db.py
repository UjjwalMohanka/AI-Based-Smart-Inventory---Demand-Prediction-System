import sys
import os
from datetime import datetime, date, timedelta
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, Product, Inventory, Sales

def seed_data():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding MySQL Database...")
        
        # 1. Create Admin User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Created user: admin/admin123")
        
        # 2. Add sample products
        products_data = [
            {'name': 'Steel Rods (12mm)', 'category': 'Metal', 'unit': 'kg', 'reorder': 500, 'stock': 800},
            {'name': 'Copper Wire (G24)', 'category': 'Metal', 'unit': 'meters', 'reorder': 1000, 'stock': 1200},
            {'name': 'Industrial Bolts (M8)', 'category': 'Hardware', 'unit': 'boxes', 'reorder': 200, 'stock': 150},
            {'name': 'PVC Pipe (4 inch)', 'category': 'Plastic', 'unit': 'units', 'reorder': 300, 'stock': 450}
        ]
        
        for p_data in products_data:
            if not Product.query.filter_by(name=p_data['name']).first():
                p = Product(
                    name=p_data['name'], 
                    category=p_data['category'], 
                    unit=p_data['unit'], 
                    reorder_point=p_data['reorder']
                )
                db.session.add(p)
                db.session.flush()
                
                inv = Inventory(product_id=p.id, quantity_in_stock=p_data['stock'])
                db.session.add(inv)
                
                # Add 12 months of historical sales
                today = date.today()
                for i in range(12):
                    sale_date = today - timedelta(days=i*30)
                    # Random base quantity with trend
                    base_qty = 400 + (12-i)*10 + random.randint(-50, 50)
                    sale = Sales(
                        product_id=p.id,
                        quantity_sold=base_qty,
                        sale_date=sale_date,
                        month=sale_date.month,
                        year=sale_date.year
                    )
                    db.session.add(sale)
                
                print(f"✓ Added product: {p_data['name']} with 12 months sales data")
        
        db.session.commit()
        print("\n✅ MySQL Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
