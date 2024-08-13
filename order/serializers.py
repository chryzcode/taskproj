from rest_framework import serializers
from .models import Order, OrderItem
from product.models import Product
from user.serializers import UserSerializer
from product.serializers import ProductDetailSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model. Handles serialization and validation of order items.
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the status of an order.
    """
    class Meta:
        model = Order
        fields = ['status']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model. Handles serialization and validation of orders,
    including nested order items.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'items')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'status')

    def create(self, validated_data):
        """
        Create a new order along with its order items.
        
        Ensures product stock is sufficient before creating order items and
        updates product stock accordingly.
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if product.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for product: {product.name}")

            product.quantity -= quantity
            product.save()

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Order model. Includes nested serialization of user and order items.
    """
    items = OrderItemSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'updated_at', 'items')

