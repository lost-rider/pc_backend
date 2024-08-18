from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, Userserializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Product

@api_view(['POST'])
def login(request):
    user= get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found."},status=status.HTTP_404_NOT_FOUND)
    serializer=Userserializer(instance=user)
    return Response({"user":serializer.data})

@api_view(['POST'])
def signup(request):
    serializer=Userserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({"user":serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def productview(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"products": serializer.data})

