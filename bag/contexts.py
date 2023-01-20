from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []   # empty list ofr contents to be stored
    total = 0        # variable for total
    product_count = 0   # variable for number of products 

    # getting  the information from the bag session, or creating an empty bag
    bag = request.session.get('bag', {})

    #addign the logic to update cost, and qunatities 
    for item_id, item_data in bag.items():
        if isinstance(item_data, int):                        #if item data has a number value DO
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,        
                'quantity': item_data,
                'product': product,        #getting the actual prodcut so we can referene later 
            })
        else:                                           # if item data doesnt have a number do this
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,        
                    'quantity': item_data,
                    'product': product,     
                    'size': size,
                })    




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