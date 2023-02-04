from django.db import models

# Create your models here.

import uuid            #used to generate order 

from django.db import models
from django.db.models import Sum        # from django to do the sum 

from django.conf import settings

from django_countries.fields import CountryField 

from products.models import Product        


class Order(models.Model):                  # this handles orders across the store 
    order_number = models.CharField(max_length=32, null=False, editable=False)         # editable = False 
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)          # null = true means can be left blank  
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)                            #adds date/time automatically
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)     # calculated field
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)       # calculated field
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)       # calculated field
    original_bag = models.TextField(null=False, blank=False, default='')   # added in case cusotmer orders smae items but on a different order
    stripe_pid = models.CharField(max_length=254, null=False, default='')   # added in case cusotmer order same items on different day


    def _generate_order_number(self):                                   # underscore at start means its aprovate methos - creates a unique order number 
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()                             # uuid is part of function imported and is the syntax used to generate order number 

    def update_total(self):       #updates total using sum function imported form django !!fried my head this bit !!
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0   #lineitems are part of using the aggregate  function syntax  imported from DJANGO
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()  #calls generate order function 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):    # individual shopping bag item linked to an order 
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')     #foreign key to order class
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)                         #foreign key to product
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'       #retrun sku for the item that is in the order   
