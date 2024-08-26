from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from product.serializers import ProductSerializer
from .models import Order, OrderItem
from product.models import Product
from django.db.models import Sum
from .serializers import OrderSerializer, OrderDetailSerializer, OrderStatusSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()



@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def order_create_or_list(request):
    """
    Create a new order or list all orders.

    POST request to create a new order.
    GET request to list all orders.
    The request must be authenticated.

  

    Returns the created order details if POST is successful.
    Returns a list of all orders if GET is successful.
    """
    if request.method == 'POST':
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            detail_serializer = OrderDetailSerializer(order)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """
    Retrieve or update order details.

    GET request to retrieve the details of a specific order.
    PUT request to update the status of a specific order (staff only).
    The request must be authenticated.

    GET request URL: /orders/<pk>/
    PUT request URL: /orders/<pk>/

 
    Returns the order details if GET is successful.
    Returns the updated order details if PUT is successful.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user.is_staff:
            serializer = OrderStatusSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                order = serializer.save()
                detailed_order = OrderDetailSerializer(order)
                return Response(detailed_order.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRecommendedProducts(request):
    # Aggregate the order items by product and sum their quantities
    ordered_products = (
        OrderItem.objects.filter(order__user=request.user)
        .values('product')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
    )

    # Get the product IDs of the most frequently ordered products
    top_product_ids = [item['product'] for item in ordered_products]

    # Fetch the recommended products (you can modify this query to suit your recommendation logic)
    recommended_products = Product.objects.filter(id__in=top_product_ids)

    # Serialize the products
    serializer = ProductSerializer(recommended_products, many=True)
    
    return Response(serializer.data)
