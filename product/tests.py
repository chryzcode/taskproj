from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Product
from order.models import Order, OrderItem
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class ProductTests(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            full_name='Admin User'
        )
        self.client.force_authenticate(user=self.admin_user)
        
        # Define URLs
        self.product_list_url = reverse('product_list')
        self.product_create_url = reverse('product_create')
        self.product_detail_url = lambda pk: reverse('product_detail', kwargs={'pk': pk})
        self.low_stock_report_url = reverse('low_stock_report')
        self.sales_report_url = reverse('sales_report') 

    def test_product_list_authenticated(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '19',  
            'quantity': 100,
            'user': self.admin_user.id
        }
        response = self.client.post(self.product_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

    def test_product_detail(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price='19', 
            quantity=100,
            user=self.admin_user
        )
        response = self.client.get(self.product_detail_url(product.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_update_admin(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price='19', 
            quantity=100,
            user=self.admin_user
        )
        update_data = {'price': '29'}  #
        response = self.client.put(self.product_detail_url(product.pk), update_data, format='json')
        
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        product.refresh_from_db()
        self.assertEqual(product.price, int("29"))  # Ensure price is updated correctly


    def test_product_delete_admin(self):
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price='19', 
            quantity=100,
            user=self.admin_user
        )
        response = self.client.delete(self.product_detail_url(product.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_low_stock_report_admin(self):
        # Create products with low stock
        Product.objects.create(name='Low Stock Product', quantity=5, price='10')  # Provide price here
        response = self.client.get(self.low_stock_report_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_sales_report_admin(self):
        # Create orders with order items
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price='19',  # Use string representation of an integer
            quantity=100,
            user=self.admin_user
        )
        order = Order.objects.create(created_at=timezone.now(), user=self.admin_user)  # Add user
        OrderItem.objects.create(order=order, product=product, quantity=2)
        response = self.client.get(self.sales_report_url)  # No period in URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
