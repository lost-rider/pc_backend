from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product

class Userserializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [ 'username','password', 'email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [ 'title', 'price', 'link', 'image_url','power_rating','value','current_rating','score','value1','value2']