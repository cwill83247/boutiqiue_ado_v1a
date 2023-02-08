from django.shortcuts import render, get_object_or_404
from django.contrib import messages                         # importing from djangos framework library
# Create your views here.

from django.shortcuts import render
from .models import UserProfile
from .forms import UserProfileForm

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