from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []   # empty list ofr contents to be stored
    total = 0        # variable for total
    product_count = 0   # variable for number of products 

    if total < settings.FREE_DELIVERY_THRESHOLD:                                        # logic to check if less than free delivery amount
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total                          
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {                                             # adding all of my items into context so avaiable across the site 
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context