from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)            # added as part of TOAST messages
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None                                         #adding for size and adding logic for sizing
    if 'product_size' in request.POST:                  # is size present in url if so assign it to the variable below 
        size = request.POST['product_size']

    bag = request.session.get('bag', {})             # this is key as creates in  he http session and stores it until user closes browser

    if size:                                                #if size has a value
        if item_id in list(bag.keys()):                                 #checking do we aleady have this item in the bag, of the same size just increase quantity
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity       # if not add an item       
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)

#adjusting/editing bag 
def adjust_bag(request, item_id):
   
    product = get_object_or_404(Product, pk=item_id)            # added as part of TOAST messages
    quantity = int(request.POST.get('quantity'))
    size = None                                         #adding for size and adding logic for sizing
    if 'product_size' in request.POST:                  # is size present in url if so assign it to the variable below 
        size = request.POST['product_size']

    bag = request.session.get('bag', {})             # this is key as creates in  he http session and stores it until user closes browser

    if size:                                                #if size has a value
       if quantity > 0:
          bag[item_id]['items_by_size'][size] = quantity
          messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
       else:
        del bag[item_id]['items_by_size'][size]
        if not bag[item_id]['items_by_size'][size]:      #if no other sizes of that item 
            bag.pop(item_id)                            #remove item from dictionairy.. pop it off
        messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')    
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
          bag.pop(item_id)                          # pop it out of the bag... 
          messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(reverse('view_bag'))    


#removing items from the bag 
def remove_from_bag(request, item_id):
   
    try:
        product = get_object_or_404(Product, pk=item_id)      #here we addign the product variable so can be used... in our messages 
        size = None                                         #adding for size and adding logic for sizing
        if 'product_size' in request.POST:                  # is size present in url if so assign it to the variable below 
            size = request.POST['product_size']
        bag = request.session.get('bag', {})             # this is key as creates in  he http session and stores it until user closes browser
            
        if size:                                                #if size has a value
            del bag[item_id]['items_by_size'][size] 
            if not bag[item_id]['items_by_size']:      #if no other sizes of that item 
                    bag.pop(item_id) 
            messages.success(request, f'Removed size {size.upper()}' f'{product.name} from your bag')    
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

            request.session['bag'] = bag
            return HttpResponse(status=200)  

    except Exception as e: 
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)     
