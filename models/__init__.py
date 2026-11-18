"""Les 8 tables de la base, importables d'un coup : from models import Product, Menu...

Importer ce paquet enregistre toutes les tables dans SQLModel.metadata,
ce qui est nécessaire avant create_all().
"""

from models.accounts import Order, OrderItem, User
from models.catalogue import ClosingDay, Menu, MenuProduct, MenuWeekday, Product

__all__ = [
    "User",
    "Product",
    "Menu",
    "MenuProduct",
    "MenuWeekday",
    "ClosingDay",
    "Order",
    "OrderItem",
]
