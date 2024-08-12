from rest_framework import serializers
from .models import Product
from user.serializers import UserSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Product
        fields = '__all__'
