from django.shortcuts import render, get_object_or_404
from .models import Product                     # importing the Prodcuts class from models.py  

# Create your views here.

def all_products(request):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    products = Product.objects.all ()                    #creating a variable called prpdcuts that holds all of the objects in Product

    context = {                                         # ??? Not sure what this does ???                            
        'products': products,

    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    product = get_object_or_404(Product, pk=product_id)                  #creating a variable called product that holds the Product

    context = {                                         # ??? Not sure what this does ???                            
        'product': product,

    }

    return render(request, 'products/product_detail.html', context)