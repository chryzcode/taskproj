from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Product
from order.models import OrderItem
from django.db.models import Sum, F
from datetime import datetime, timedelta
from django.utils import timezone
from order.models import Order
from .serializers import *
from user.permissions import IsAdminOrReadOnly

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductDetailSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save(user=request.user)
        detail_serializer = ProductDetailSerializer(product)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrReadOnly])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            detail_serializer = ProductDetailSerializer(product)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def low_stock_report(request):
    low_stock_products = Product.objects.filter(quantity__lt=10)
    serializer = LowStockProductSerializer(low_stock_products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def sales_report(request, period='day'):
    if period == 'day':
        start_date = timezone.now().date() - timedelta(days=1)
    elif period == 'week':
        start_date = timezone.now().date() - timedelta(weeks=1)
    elif period == 'month':
        start_date = timezone.now().date() - timedelta(days=30)
    else:
        return Response({"error": "Invalid period"}, status=status.HTTP_400_BAD_REQUEST)

    orders = Order.objects.filter(created_at__gte=start_date)

    report_data = orders.annotate(date=F('created_at__date')) \
                        .values('date') \
                        .annotate(
                            total_sales=Sum(F('items__quantity') * F('items__product__price')),
                            total_quantity=Sum('items__quantity')
                        ) \
                        .values('date', 'total_sales', 'total_quantity')

    serializer = SalesReportSerializer(report_data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)