from django.shortcuts import render
from .models import Product                     # importing the Prodcuts class from models.py  

# Create your views here.

def all_products(request):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    products = Product.objects.all ()                    #creating a variable called prpdcuts that holds all of the objects in Product

    context = {                                         # ??? Not sure what this does ???                            
        'products': products,

    }

    return render(request, 'products/products.html', context)
