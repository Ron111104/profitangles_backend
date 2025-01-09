"""
URL configuration for profitangles_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import hello
from stocks.views import StockDataView
from .visualize.views.upload import upload_file
from .views.stock_open_price import stock_open_price
from .views.rsi_graph import rsi_graph
from .views.max_percentage import max_percentage_movement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello, name='hello'),
    path('api/stocks/<str:symbol>/', StockDataView.as_view(), name='stock-data'),
    # path('visualize/', include('visualize.urls')),
    path('upload/', upload_file, name='upload_file'),
    path('stock_open_price/', stock_open_price, name='stock_open_price'),
    path('rsi_graph/', rsi_graph, name='rsi_graph'),
    path('max_percentage_movement/', max_percentage_movement, name='max_percentage_movement'),
]

from django.urls import path


urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('stock_open_price/', stock_open_price, name='stock_open_price'),
    path('rsi_graph/', rsi_graph, name='rsi_graph'),
    path('max_percentage_movement/', max_percentage_movement, name='max_percentage_movement'),
]
