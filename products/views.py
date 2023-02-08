from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages              # had to improt this as part of search 
from .models import Product, Category                     # importing the Prodcuts class from models.py  
from django.db.models import Q 
from django.db.models.functions import Lower

 #just importing classes that we need
from .forms import ProductForm

# Create your views here.

def all_products(request):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    products = Product.objects.all ()                    #creating a variable called prpdcuts that holds all of the objects in Product
    query = None                                    # added as part of search to set variable to none
    categories = None                           # added as part of Categories 
    sort = None
    direction = None


    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':             #ythis part is to allow lowercase 
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))     
            if sortkey == 'category':           # added this and line beloew so sorting by categorry name rather than category id
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'                #changes order form ascending to descending using f - 
            products = products.order_by(sortkey)        #order_by method is part of DJANOGO
        
                                               # start of search element 
        if 'category' in request.GET:                       # category specific 
            categories = request.GET['category'].split(',')   # splits categoreis url passed by , 
            products = products.filter(category__name__in=categories)  # note the double underscore its part of DJANGO syntax  for queries works beause of foriegn key 
            categories = Category.objects.filter(name__in=categories)    # this is done so we can see what category or category was selected 

        if 'q' in request.GET:                            # we have set q as the text input in the form - hence why we use q here   
            query = request.GET['q']                        # value of q gets set to a variable called query --- 
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)    # Q is part of DJANGO and allows an OR search so searches in description or name fields , note the i at the start
            products = products.filter(queries)                                       #end of search element  return prpdcuts based on queries variable
                                                  
    current_sorting = f'{sort}_{direction}'             #part of sort and direction                                         

    context = {                                         # ??? Not sure what this does ???                            
        'products': products,
        'search_term': query,                           # added for search ? unsure why 
        'current_categories': categories,          # variable created and referances categoreis in line 18  
        'current_sorting': current_sorting,       # added as part of sort ---  so uses above to define a default direction
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):                                  #creating a function called all_prodcuts
    """ A view to return prodcuts, sort and search """

    product = get_object_or_404(Product, pk=product_id)                  #creating a variable called product that holds the Product

    context = {                                         # ??? Not sure what this does ???                            
        'product': product,

    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()                            #calling product form class form forms.py creating an instance called form 
    template = 'products/add_product.html'
    context = {
        'form': form,                                       #form is just variable name we have given it
    }

    return render(request, template, context)        # we mash up the template and context to output html @ add_prpdcut.html