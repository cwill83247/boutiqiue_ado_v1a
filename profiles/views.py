from django.shortcuts import render, get_object_or_404
from django.contrib import messages                         # importing from djangos framework library
# Create your views here.

from django.shortcuts import render
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required    # imported to secure superuser views !!!!!
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':   #post handler for when profile updated 
        form = UserProfileForm(request.POST, instance=profile)                      #userprofile form comes from the IMPORt at the top so imports class
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    
    form = UserProfileForm(instance=profile)
    orders =profile.orders.all()


    template = 'profiles/profile.html'
    context = {
        'form':form,
        'orders':orders,
    }

    return render(request, template, context)

def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'  ##using this as our template as already has what we need
    context = {
        'order': order,                   #  value pair the first part of the pair could be anything and its what we call in our page
        'from_profile': True,
    }

    return render(request, template, context)    