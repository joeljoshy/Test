from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)


    def __str__(self):
        return self.brand_name

class Seller_Details(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    address = models.TextField()
    bank_name = models.CharField(max_length=100)
    account_number = models.IntegerField()
    ifsc_code = models.CharField(max_length=20)

    def __str__(self):
        return self.username




class Products(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    offer = models.FloatField()

    def __str__(self):

        return self.product_name
class ProductImage(models.Model):
    product = models.ForeignKey(Products,default=None,on_delete=models.CASCADE)
    images = models.FileField(upload_to='images')

    def __str__(self):
        return self.product.product_name