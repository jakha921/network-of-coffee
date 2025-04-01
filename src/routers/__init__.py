from .users import router as users
from .products import router as products
from .categories import router as categories
from .orders import router as orders
from .cart import router as cart
from .chat import router as chat
from .static import router as static

__all__ = ['users', 'products', 'categories', 'orders', 'cart', 'chat', 'static'] 