from django.urls import path
from . import views
from .views.fetch_stock_data import fetch_stock_data
from .views.ohlc import ohlc_graph
from .views.stock_open_price import stock_open_price
from .views.rsi_graph import rsi_graph
from .views.max_percentage import max_percentage_movement
from .views.generate_image import generate_image  # New import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('rsi_graph/', rsi_graph, name='rsi_graph'),
    path('stock_open_price/', stock_open_price, name='stock_open_price'),
    path('max_percentage_movement/', max_percentage_movement, name='max_percentage_movement'),
    path('fetch_stock_data/', fetch_stock_data, name='fetch_stock_data'),
    path('ohlc/', fetch_stock_data, name='ohlc_graph'),
    path('images/', generate_image, name='generate_image'),  # New route
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
