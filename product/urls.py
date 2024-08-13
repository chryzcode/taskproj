from django.urls import path
from .views import *


urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<uuid:pk>/', product_detail, name='product_detail'),
    path('reports/low-stock/', low_stock_report, name='low_stock_report'),
    path('reports/sales/', sales_report, name='sales_report'),
]