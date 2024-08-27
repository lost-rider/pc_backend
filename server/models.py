# models.py
from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255,null=True, blank=True)
    power_rating = models.CharField(max_length=5,null=True, blank=True)
    current_rating = models.CharField(max_length=5,null=True, blank=True)
    value = models.CharField(max_length=5,null=True, blank=True)
    price = models.CharField(max_length=50,null=True, blank=True)
    link = models.URLField(max_length=200,null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.title or 'No Title'
    
class User(models.Model):
    username = models.CharField(max_length=255,null=True, blank=True)
    password = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.username
