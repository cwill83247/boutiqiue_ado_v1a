from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
            else:
                bag[item_id]['items_by_size'][size] = quantity       # if not add an item       
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
    