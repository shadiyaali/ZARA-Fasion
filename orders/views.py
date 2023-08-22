from django.shortcuts import render,redirect
from django.shortcuts import render,redirect
from cart.models import Cart,CartItem
import random
from store.models import Product,Profile
from mainapp.models import Order,OrderItem
from django.contrib import messages
from accounts.models import Account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
import json


 




# @login_required(login_url=('login')) 
# def placeorder(request):
#     if request.method =='POST':

#         #cart check
#         # cart_items   = CartItem.objects.filter(user=request.user.id)
#         # if not cart_items:
#         #     return redirect('store')
#         user = request.user.id

#         currentuser = Account.objects.get(id=user)
        
#         if not currentuser.first_name : # type: ignore
#             currentuser.first_name = request.POST.get('first_name')# type: ignore
#             currentuser.last_name = request.POST.get('last_name')# type: ignore
#             currentuser.save()# type: ignore
#             # print(currentuser.first_name)# type: ignore


#         if not Profile.objects.filter(user=request.user):

#             userprofile = Profile.objects.create(
#                 user = request.user,
#                 phone = request.POST['phone'],
#                 address = request.POST['address'],
#                 city = request.POST['city'],
#                 state= request.POST['state'],
#                 country = request.POST['country'],
#                 pincode = request.POST['pincode'],

#             )
#             # userprofile.user = request.user
#             # userprofile.phone = request.POST['phone']
#             # userprofile.address = request.POST['address']
#             # userprofile.city = request.POST['city']
#             # userprofile.state= request.POST['state']
#             # userprofile.country = request.POST['country']
#             # userprofile.pincode = request.POST['pincode']
#             # userprofile.save()   
             
#         user=request.user
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         address = request.POST['address']
#         city = request.POST['city']
#         state= request.POST['state']
#         country = request.POST['country']
#         pincode = request.POST.get('pincode')


#         cart_items   = CartItem.objects.filter(user=request.user)
#         total = 0
#         grand_total = 0
#         for cart_item in cart_items:
#             total    += (cart_item.product.price * cart_item.quantity)  

#         tax = (2 * total)/100
#         grand_total = total + tax

#         trackNo = 'ecom'+str(random.randint(1111111,9999999))
#         while Order.objects.filter(tracking_no=trackNo) is None:
#             trackNo = 'ecom'+str(random.randint(1111111,9999999))


#         newOrder = Order.objects.create(
#             user =user,
#             first_name = first_name,
#             last_name=last_name,
#             email = email,
#             phone = phone,
#             address = address,
#             city = city,
#             state = state,
#             country = country,
#             pincode = pincode,
#             total_price = grand_total,
#             tracking_no = trackNo

            
#         )

#         newOrderItems = CartItem.objects.filter(user=request.user)
#         for item in newOrderItems:
#             OrderItem.objects.create(
#                 user = request.user,
#                 order = newOrder,
#                 product=item.product,
#                 price=item.product.price,
#                 quantity=item.quantity,
                
#             )
#             orderproduct = Product.objects.filter(id=item.product_id).first()
#             orderproduct.stock = orderproduct.stock - item.quantity 
#             orderproduct.save()
            
#         CartItem.objects.filter(user=request.user).delete()

#         messages.success(request, 'Your order has been placed successfully')

        
    


#     return redirect('store')   
# @never_cache
# @login_required(login_url=('login'))  # type: ignore
# def razorpaycheck(request):
#     cart = CartItem.objects.filter(user=request.user)  
#     total_price = 0 
#     if cart:
            
#         for item in cart:
#             total_price   += (item.product.price * item.quantity)

#         return JsonResponse({
#             'grand_total' : total_price
           

#         })
#     else:
#         return redirect('store')    
@never_cache
@login_required(login_url=('login')) 
def placeorder(request):
    if request.method =='POST':

        #cart checkpru
        print('here')
        cart_items   = CartItem.objects.filter(user=request.user.id)
        if not cart_items:
            return redirect('store')

        currentuser = Account.objects.filter(id=request.user.id).first()
        if not currentuser.first_name : # type: ignore
            currentuser.first_name = request.POST.get('first_name')# type: ignore
            currentuser.last_name = request.POST.get('last_name')# type: ignore
            currentuser.save()# type: ignore
            print(currentuser.first_name)# type: ignore


        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state= request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()   
             

        newOrder =Order()
        newOrder.user=request.user
        newOrder.first_name = request.POST.get('first_name')
        newOrder.last_name = request.POST.get('last_name')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state= request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')
        newOrder.payment_mode = request.POST.get('payment_mode')
        newOrder.payment_id = request.POST.get('payment_id')
        
        #taking total price
        cart_items   = CartItem.objects.filter(user=request.user)
        total = 0
        for cart_item in cart_items:
            total    += (cart_item.product.price * cart_item.quantity)

        tax = (2 * total) / 100
        grand_total = tax + total
        newOrder.total_price = grand_total 
        print(total)
        trackNo = 'zara'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackNo) is None:
            trackNo = 'zara'+str(random.randint(1111111,9999999))
        newOrder.tracking_no=trackNo
        newOrder.sub_total=total
        newOrder.tax=tax
        newOrder.save()

        newOrderItems = CartItem.objects.filter(user=request.user)
        for item in newOrderItems:
            OrderItem.objects.create(
                order = newOrder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                user=request.user
            )
            #TO DECRESE THE QUANTITY OF PRODUCT
            orderproduct = Product.objects.filter(id=item.product_id).first() # type: ignore
            orderproduct.stock -=  item.quantity # type: ignore
            orderproduct.save() # type: ignore
        
        print('after neworder')
            
        # TO CLEAR THE USER'S CART
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request,'Order Placed Successfully')
        
    payMode =  request.POST.get('payment_mode')
    print(request.POST.get('payment_mode'))
    if (payMode == "Paid by Razorpay" ):
       
        return JsonResponse ({'status':"Your order has been placed successfully"})
    elif (payMode == "COD" ):
        return redirect('myorder')
    return redirect('checkout') 

@never_cache
@login_required(login_url=('login'))  # type: ignore
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)  
    total_price = 0 
    if cart:
            
        for item in cart:
            total_price   += total_price + item.product.price * item.quantity 
        tax = round((2 * total_price)/100)
        grand_total = total_price + tax
            

        return JsonResponse({
            'total_price' : grand_total

        })
    else:
        return redirect('store')

@never_cache
@login_required(login_url=('login')) 
def myorder(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')
    context ={
        'orders':orders
    }
    return render(request,'orders/myorder.html',context)


@never_cache
@login_required(login_url=('login')) 
def vieworder(request,tracking_no):
    order =Order.objects.filter(tracking_no=tracking_no,user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
        
    }
    return render(request,'orders/vieworder.html',context)


def cancel_order(request,tracking_no):
    order =Order.objects.get(tracking_no=tracking_no,user=request.user)
    order.status ='Cancelled'
    order.save()
    return redirect('myorder')

   
def order_complete(request):
     
    payment_id = request.GET.get('payment_id')

    order_details = Order.objects.get(payment_id=payment_id)
    orderitems = OrderItem.objects.filter(order=order_details.id)
     
    context={
        'orders': order_details,
        'orderitems':orderitems,
         
    }
        
    return render(request, 'orders/order_complete.html',context)
  
              