from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Order, OrderLineItem   # being imported form Models.py 


class OrderLineItemAdminInline(admin.TabularInline):   # inherits from admin.tabularinline       we can see a listof line items editable  
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):                             #order admin class with read only fields 
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'date', 'full_name',              # editable fields 
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)                                       #most recent orders at the top 

admin.site.register(Order, OrderAdmin)