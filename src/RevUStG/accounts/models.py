from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models import CheckConstraint, Q, F

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
    order_id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = 'O', primary_key = True)
    customer = models.OneToOneField(Customer, null = True, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return self.order_id


class Tag(models.Model):
    tag = models.CharField(max_length= 50, null= True)

    def __str__(self) -> str:
        return self.tag

class Platform(models.Model):
    platform = models.CharField(max_length= 100, null= True)
    platform_icon = models.ImageField(null=True, default="default_product_image.jpg", blank=True)

    def __str__(self) -> str:
        return self.platform

class Product(models.Model):
    id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = "PD", primary_key = True)
    tag = models.ManyToManyField(Tag)
    name = models.CharField(max_length=100, null=True)
    sell_price = models.FloatField(null=True)
    rent_price = models.FloatField(null=True)
    cover_img = models.ImageField(null=True, blank=True, default='default_product_image.jpg')
    avt_img = models.ImageField(null=True, blank=True, default='default_product_image.jpg')
    platForm = models.ForeignKey(Platform, null=True,on_delete=models.SET_NULL)
    publisher = models.CharField(max_length= 100, null=True)
    description = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name
    

class OrderProduct(models.Model):
    TYPE = (('Rent', 'Rent'),
            ('Buy', 'Buy')
            )

    id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = 'OP', primary_key = True)
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default= 0, null=True)
    type = models.CharField(max_length=30, null=True, choices=TYPE, default=TYPE[1])

    def __str__(self) -> str:
        return self.id

class Account(models.Model):
    STATUS = (('Rented', 'Rented'), 
              ('Available', 'Available'),
              ('Sold', 'Sold')
              )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, default= STATUS[1])
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = 'A', primary_key = True)

    def __str__(self) -> str:
        return self.username


class PurchasedItem(models.Model):
    customer = models.CharField(max_length=100, null=True)
    time = models.DateField(null = True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null= True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    item_id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = "PUR")



    def __str__(self) -> str:
        return str(self.item_id)
    

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(null=True, default= 'default_product_image.jpg',blank=True)

    class Meta:
        verbose_name_plural = "Product Image"

class FavoriteProduct(models.Model):
    id = ShortUUIDField(unique = True, length = 10, max_length =30, prefix = 'FP', primary_key = True)
    customer = models.CharField(max_length = 100, null=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)


MOBILE_CARRIER_CHOICE = (('Viettel' , 'Viettel'), ('Mobifone', 'Mobifone'), ('Vinaphone', 'Vinaphone'))
VALUE = ((10000, 10000), (20.000, 20000), (50000, 50000), (100000, 100000), (200000, 200000), (500000, 500000))

class PhoneCardPayment(models.Model):
    id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = 'PCP', primary_key = True)
    mobile_carrier = models.CharField(choices=MOBILE_CARRIER_CHOICE, null=True, max_length=100)
    serial_code = models.CharField(max_length=15, null = True, help_text='15 Digits')
    card_code = models.CharField(max_length=14, null=True, help_text='14 Digits')
    value = models.PositiveIntegerField(choices=VALUE, default=0)

BANK = (('Agribank', 'Agribank'), ('Vietcombank', 'Vietcombank'), ('MBBank', 'MBBank'))
class BankAccountPayment(models.Model):
    id = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = 'BAP', primary_key = True)
    bank = models.CharField(max_length=100, choices=BANK, null=True)
    account = models.CharField(max_length=14, null=True, help_text='9 to 14 digits')
    value = models.PositiveIntegerField(default=0, null=True)




   



