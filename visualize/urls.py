# visualize/urls.py
from django.urls import path
from . import views
from .views.upload import upload_file
from .views.stock_open_price import stock_open_price
from .views.rsi_graph import rsi_graph
from .views.max_percentage import max_percentage_movement
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('upload/', views.visualize_stock_data, name='visualize_stock_data'),
    path('upload/', upload_file, name='upload'),
    path('rsi_graph/', rsi_graph, name='rsi_graph'),
    path('stock_open_price/', stock_open_price, name='stock_open_price'),
    path('max_percentage_movement/', max_percentage_movement, name='max_percentage_movement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)