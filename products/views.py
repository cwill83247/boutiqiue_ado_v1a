from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages              # had to improt this as part of search 
from .models import Product                     # importing the Prodcuts class from models.py  
from django.db.models import Q 

# Create your views here.

def all_products(request):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    products = Product.objects.all ()                    #creating a variable called prpdcuts that holds all of the objects in Product
    query = None                                    # added as part of search to set variable to none


    if request.GET:                                       # start of search element 
        if 'q' in request.GET:                            # we have set q as the text input in the form - hence why we use q here   
            query = request.GET['q']                        # value of q gets set to a variable called query --- 
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)    # Q is part of DJANGO and allows an OR search so searches in description or name fields , note the i at the start
            products = products.filter(queries)                                     #end of search element  return prpdcuts based on queries variable

    context = {                                         # ??? Not sure what this does ???                            
        'products': products,
        'search_term': query,                           # added for search ? unsure why 

    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    product = get_object_or_404(Product, pk=product_id)                  #creating a variable called product that holds the Product

    context = {                                         # ??? Not sure what this does ???                            
        'product': product,

    }

    return render(request, 'products/product_detail.html', context)