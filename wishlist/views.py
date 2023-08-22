from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import WishlistItems
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
# from store.models import Variation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.



@login_required(login_url='login')
def add_to_wishlist(request,id):
    user = request.user
    product = Product.objects.get(id=id)

    is_wished = WishlistItems.objects.filter(product=product,user=user)
    if not is_wished:
        
        product = WishlistItems.objects.create(
            user=user,
            product=product,
            is_active=True,
        )
        return redirect('wishlist')
    
    else:
        return redirect('wishlist')

@login_required(login_url='login')
def wishlist(request):
    products = WishlistItems.objects.filter(user=request.user,is_active=True)
    context={
        'products':products,
    }
    return render(request, 'wishlist/wishlist.html', context)
def delete_from_wishlist(request,id):
    wishlist_item = WishlistItems.objects.get(id=id)
    wishlist_item.delete()
    return redirect('wishlist')  
