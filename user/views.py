from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    
    Accepts POST requests with 'email', 'full_name', and 'password'.
    Returns a success message if the user is registered successfully.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Log in an existing user.
    
    Accepts POST requests with 'email' and 'password'.
    Returns a success message if the user is logged in successfully.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        auth_login(request, user)
        return Response({'detail': 'User logged in successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Log out the current user.
    
    Accepts POST requests.
    Returns a success message if the user is logged out successfully.
    """
    auth_logout(request)
    return Response({'detail': 'User logged out successfully'}, status=status.HTTP_200_OK)
