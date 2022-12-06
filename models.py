from distutils.command.upload import upload
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.forms import SelectMultiple


class User(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.username


       



class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self) :
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self) :
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self) :
        return self.name



class Product(models.Model):
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/")
    pointure = models.PositiveBigIntegerField(max_length=2, null=True, blank=True)

    cart = models.ManyToManyField(User, related_name='cart', default=None, blank = True)
    wishlist = models.ManyToManyField(User, related_name='favourite', default=None, blank = True)

    is_delivering = models.BooleanField(default=False)

    sold = models.BooleanField(default=False)
    show_info = models.BooleanField(default=False)

    
  
    description = models.TextField(null=True, blank=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self) :
        return self.name         