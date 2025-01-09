# visualize/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.visualize_stock_data, name='visualize_stock_data'),
]
