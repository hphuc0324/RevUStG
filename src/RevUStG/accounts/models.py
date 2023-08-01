from django.db import models
from django.contrib.auth.models import User

# Create your models here.

DEFAULT_DESCRIPTION = "A new member of RevustG"

#Customer class - store user's basic information
class Customer(models.Model):
    SEX = (('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
           )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length= 50, null=True)
    sex = models.CharField(max_length= 10, default= 'Male',choices=SEX)
    phone_number = models.CharField(max_length= 10, null= True)
    dob = models.DateField(null=True)
    coins = models.IntegerField(null=True, default=0)
    profile_image = models.ImageField(null= True, default="default_user_image.jpeg", blank=True)
    description = models.TextField(null=True, default= DEFAULT_DESCRIPTION, max_length= 100)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    customer = models.OneToOneField(Customer, null = True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return str('Order of' + self.customer.__str__)  


class Tag(models.Model):
    tag = models.CharField(max_length= 50, null= True)

    def __str__(self) -> str:
        return self.tag

class Platform(models.Model):
    platform = models.CharField(max_length= 100, null= True)

    def __str__(self) -> str:
        return self.platform

class Product(models.Model):
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=100, null=True)
    sell_price = models.FloatField(null=True)
    rent_price = models.FloatField(null=True)
    cover_img = models.ImageField(null=True, blank=True)
    platForm = models.ForeignKey(Platform, null=True,on_delete=models.SET_NULL)
    publisher = models.CharField(max_length= 100, null=True)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default= 0, null=True)

    def __str__(self) -> str:
        return self.product.__str__

class Account(models.Model):
    STATUS = (('Rented', 'Rented'), 
              ('Available', 'Available'),
              ('Sold', 'Sold')
              )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default= STATUS[1])
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    id = models.CharField(max_length= 15, primary_key=True)

    def __str__(self) -> str:
        return self.username


class PurchasedItem(models.Model):
    customer = models.CharField(max_length=100, null=True)
    time = models.DateField(null = True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null= True)
    item_id = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return str(self.item_id)



