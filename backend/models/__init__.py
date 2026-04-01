from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .product import Product
from .inventory import Inventory
from .sales import Sales
from .prediction import Prediction

__all__ = ['db', 'User', 'Product', 'Inventory', 'Sales', 'Prediction']
