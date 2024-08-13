from django.urls import path
from .views import *

urlpatterns = [
    path('', order_create_or_list, name='order_create'),
    path('<uuid:pk>/', order_detail, name='order_detail'),
]
