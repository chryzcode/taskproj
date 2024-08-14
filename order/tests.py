from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from product.models import Product
from django.urls import reverse
import uuid

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword',
            full_name='Admin User'
        )
        self.client.force_authenticate(user=self.admin_user)

        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=19,  # Ensure price is an integer
            quantity=100,
            user=self.admin_user
        )

        # Define URLs
        self.order_create_or_list_url = reverse('order_create_or_list')
        self.order_detail_url = lambda pk: reverse('order_detail', kwargs={'pk': pk})

    def test_order_create(self):
        data = {
            'items': [
                {
                    'product': self.product.id,
                    'quantity': 3
                }
            ]
        }
        response = self.client.post(self.order_create_or_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.exists())

    def test_order_list(self):
        # Create an order
        order = Order.objects.create(
            user=self.admin_user,  # Add user since it's a required field
            status='Pending',      # Add status if it's a required field
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=3)  # Add order item
        response = self.client.get(self.order_create_or_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure we have at least one order

    def test_order_detail_retrieve(self):
        # Create an order
        order = Order.objects.create(
            user=self.admin_user,  # Add user
            status='Pending',      # Add status
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=3)  # Add order item
        response = self.client.get(self.order_detail_url(order.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'][0]['product'], self.product.id)
        self.assertEqual(response.data['items'][0]['quantity'], 3)

    def test_order_detail_update_status(self):
        # Create an order
        order = Order.objects.create(
            user=self.admin_user,  # Add user
            status='Pending',      # Add status
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=3)  # Add order item
        update_data = {
            'status': 'completed'  # Only update the status
        }
        response = self.client.put(self.order_detail_url(order.pk), update_data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print("Response Data:", response.data)  # Print response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        # Check if the status was updated
        self.assertEqual(order.status, 'completed')
        # Ensure items remain unchanged
        self.assertEqual(order.items.first().quantity, 3)

    def test_order_detail_not_found(self):
        invalid_uuid = uuid.uuid4()  # Generate a UUID that is not used
        response = self.client.get(self.order_detail_url(invalid_uuid))  # Use the generated UUID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
