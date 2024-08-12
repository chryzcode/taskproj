from django.urls import path
from .views import *


urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<uuid:pk>/', product_detail, name='product_detail'),
]