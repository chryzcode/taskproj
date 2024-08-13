from rest_framework import serializers
from .models import Product
from user.serializers import UserSerializer

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Handles serialization and deserialization of Product objects.
    """
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Product model.
    Includes nested serialization of the user who created the product.
    """
    user = UserSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class LowStockProductSerializer(serializers.ModelSerializer):
    """
    Serializer for low stock products.
    Includes only the essential fields for low stock reporting.
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'quantity')


class SalesReportSerializer(serializers.Serializer):
    """
    Serializer for sales report data.
    Handles serialization of sales report with date, total sales, and total quantity fields.
    """
    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = serializers.IntegerField()