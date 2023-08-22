from django.shortcuts import render

# Create your views here.

import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import  logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.cache import never_cache
from . forms import MultipleImagesForm

from django.db.models import Q 

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from accounts.models import Account
from Ecomm import settings
from category.models import Category

from adminpanel.forms import ProductForm, CategoryForm
from store.models import Product, Variation,ReviewRating
from adminpanel.forms import ProductForm, CategoryForm, VariationForm
from mainapp.models import  Order, OrderItem


from django.views.generic import TemplateView
import csv
from django.http import JsonResponse, HttpResponse

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

from store.models import Product, MultipleImages




def pdf_report_create(request):
    orders = OrderItem.objects.all()
    orders = Order.objects.filter(is_ordered=True).order_by('-order_number')

    template_path = 'manager/pdf.html'

    context = {'orders': orders}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




@never_cache
@login_required(login_url='manager_login')
def manager_dashboard(request):
    if request.user.is_admin:

        user_count = Account.objects.filter(is_admin=False).count()
        category_count = Category.objects.all().count()


        context = {
            'user_count'    : user_count

        }

    return render(request, 'manager/manager_dashboard.html', context)








#PRODUCT Management
@never_cache
@login_required(login_url='manager_login')
def manage_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword'] 
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(slug__icontains=keyword) | Q(category__category_name__icontains=keyword)).order_by('id')

        else:
            products = Product.objects.all().order_by('id')

        paginator = Paginator(products, 10)
        page      = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products' : paged_products 
        }

        return render(request, 'manager/product_management.html', context)

    else:
        return redirect('home')




# DELETE Product
@never_cache
@login_required(login_url='manager_login')
def delete_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('manage_product')

    else:
        return redirect('home')



#ADD Product
@never_cache
@login_required(login_url='manager_login')
def add_product(request):
    if request.user.is_admin:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save() 
                return redirect('manage_product')
            else:
              print(form.errors)
              form = ProductForm()
              context = {
                  'form' : form
              }
              return render(request, 'manager/add_product.html', context)
        else:
            form = ProductForm()
            context = {
                'form' : form
            }
            return render(request, 'manager/add_product.html', context)

    else:
        return redirect('home')


# EDIT Product
@never_cache
@login_required(login_url='manager_login')
def edit_product(request, product_id):
    if request.user.is_admin:
        product = Product.objects.get(id=product_id)
        form = ProductForm(instance=product)

        if request.method == 'POST':
            try:
                form =ProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()

                    return redirect('manage_product')

            except Exception as e:
                raise e

        context = {
            'product' : product,
            'form' : form
        }
        return render(request, 'manager/edit_product.html', context)

    else:
        return redirect('home')



#CATEGORY Management
@never_cache
@login_required(login_url='manager_login')
def manage_category(request):
    if request.user.is_admin:
        if request.method == 'POST':
            keyword = request.POST['keyword']
            categories = Category.objects.filter(Q(category_name__icontains=keyword) | Q(slug__icontains=keyword)).order_by('id') 
        
        else:
            categories = Category.objects.all().order_by('id')

        paginator = Paginator(categories, 10)
        page = request.GET.get('page')
        paged_categories = paginator.get_page(page)

        context = {
            'categories': paged_categories
        }

        return render(request, 'manager/category_management.html', context)

    else:
        return redirect('home')

#ADD Category
@never_cache
@login_required(login_url='manager_login')
def add_category(request):
  if request.user.is_admin:
    form = CategoryForm()
    if request.method == 'POST':
      try:
        form = CategoryForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
          form.save()
        return redirect('manage_category')
      
      except Exception as e:
        raise e
    
    return render(request, 'manager/category_add.html', {'form': form})
  
  else:
    return redirect('home')



#DELETE Category
@never_cache
@login_required(login_url='manager_login')
def delete_category(request, category_id):
    if request.user.is_admin:
        category = Category.objects.get(id=category_id)
        category.delete()

        return redirect('manage_category')

    else:
        return redirect('home')





# USER Management
@never_cache
@login_required(login_url='manager_login')
def manage_user(request):
  if request.user.is_admin:
    if request.method == 'POST':
      keyword = request.POST['keyword']
      users = Account.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(phone_number__icontains=keyword)).order_by('id')
    
    else:
        users = Account.objects.filter(is_admin=False).order_by('id')

    paginator   = Paginator(users, 10) 
    page        = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users' : paged_users,
    }
    return render(request, 'manager/user_management.html', context)

  else:
    return redirect('home') 

def redirect_to_login(request):
  return redirect('manager_login')

#BAN User
@never_cache
@login_required(login_url='manager_login')
def ban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = False
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')


#UnBAN User
@never_cache
@login_required(login_url='manager_login')
def unban_user(request, user_id):
    if request.user.is_admin:
        user = Account.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return redirect('manage_user')

    else:
        return redirect('home')







@never_cache
def manager_logout(request):
    logout(request)
    return redirect('login')



@never_cache
@login_required(login_url='manager_login')
def admin_change_password(request):
  if request.user.is_admin:
    if request.method == 'POST':
      current_user = request.user
      current_password = request.POST['current_password']
      password = request.POST['password']
      confirm_password = request.POST['confirm_password']
      
      if password == confirm_password:
        if check_password(current_password, current_user.password):
          if check_password(password, current_user.password):
            messages.warning(request, 'Current password and new password is same')
          else:
            hashed_password = make_password(password)
            current_user.password = hashed_password
            current_user.save()
            messages.success(request, 'Password changed successfully')
        else:
          messages.error(request, 'Wrong password')
      else:
        messages.error(request, 'Passwords does not match')
    
    return render(request, 'manager/admin_change_password.html')
  
  else:
    return redirect('home')






   




 

#ORDER MANAGEMENT
def order_management(request):
  if request.user.is_superadmin:
    if request.method == 'POST':
        key = request.POST['key']
        order = Order.objects.filter( Q(tracking_no_startswith=key) | Q(useremailstartswith=key) | Q(first_name_startswith=key)).order_by('-id')
    else:
        order = Order.objects.all().order_by('-id') 
    paginator = Paginator(order, 10)
    page = request.GET.get('page')
    paged_order = paginator.get_page(page)

    context = {
        'order': paged_order
        }
    return render(request, 'manager/order_management.html',context)
  else:
    return redirect('index')  

#VIEW MANAGEMENT ORDER
def manager_vieworder(request,tracking_no):
  if request.user.is_superadmin:
    order = Order.objects.filter(tracking_no=tracking_no).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order': order,
        'orderitems':orderitems,
    }
    return render(request,'manager/manager_vieworder.html',context)
  else:
    return redirect('index') 

#ACCEPT ORDER
def manager_accept_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Out For Shipping'
    order.save()
    return redirect('order_management')  

#SHIP ORDER    
def manager_ship_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Shipped'
    order.save()
    return redirect('order_management')

#DELIVERED ORDER
def manager_delivered_order(request, tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Delivered'
    order.save()
    return redirect('order_management')          

#CANCEL ORDER
def manager_cancel_order(request,tracking_no):
    order = Order.objects.get(tracking_no=tracking_no)
    order.status = 'Cancelled'
    order.save()
    return redirect('order_management')


 
# VARIATION MANAGEMENT
def variation_management(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        variations = Variation.objects.filter(Q(product_product_name__icontains=keyword) | Q(
            variation_category__icontains=keyword) | Q(variation_value__icontains=keyword)).order_by('id')

    else:
        variations = Variation.objects.all().order_by('id')

    paginator = Paginator(variations, 15)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations': paged_variations
    }
    return render(request, 'manager/variation_management.html', context)

# ADD VARIATION
def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variation_management')
        else:
         messages.error(request,'Invalid form')
         return redirect('add_variation')    

    else:
        form = VariationForm()

    context = {
        'form': form
    }
    return render(request, 'manager/add_variation.html', context)

#UPDATE VARIATION
def update_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_management')
        else:
          messages.error(request,'Invalid form') 
          return redirect('update_variation')     
    else:
        form = VariationForm(instance=variation)
    context = {
        'variation': variation,
        'form': form
    }
    return render(request, 'manager/update_variation.html', context)

#DELETE VARIATION
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    variation.delete()
    return redirect('variation_management')  


 

#MULTIPLE IMAGES MANAGEMENT
@never_cache
@login_required(login_url='signin')
def multiple_image_management(request):
  multipleimages = MultipleImages.objects.all().order_by('id')
  paginator = Paginator(multipleimages, 10)
  page = request.GET.get('page')
  multipleimages = paginator.get_page(page)

  context = {
    'multipleimages': multipleimages
  }
  return render(request, 'manager/multiple_image_management.html', context)
  
#ADD MULTIPLE IMAGES
@never_cache
@login_required(login_url='lognin')
def add_multiple_images(request):  # type: ignore
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.error(request,'')
      return redirect('add_multiple_images')
    else:
      print(form.errors)
      messages.error(request,'Invalid form') 
      return redirect('add_multiple_images') 
  else:
    form = MultipleImagesForm()

  context = {
    'form': form
  }
  return render(request,'manager/add_multiple_images.html',context)


 # UPDATE MULTIPLE IMAGE
@never_cache
@login_required(login_url='login')
def update_multiple_images(request,multi_id):
  multipleimages = MultipleImages.objects.get(id=multi_id)
  form = MultipleImagesForm(instance = multipleimages)
  if request.method == 'POST':
    form = MultipleImagesForm(request.POST, request.FILES, instance = multipleimages)
    if form.is_valid():
      form.save()
      messages.success(request,'Added Succefully')
      return redirect('multiple_image_management')
    else:
      messages.error(request,'Invalid form') 
      return redirect('update_multiple_images')   
  context = {
    'form':form
  }
  return render(request, 'manager/update_multiple_images.html', context)


# DELETE MULTIPLEIMAGES
@never_cache
@login_required(login_url='login')
def delete_multiple_images(request, multi_id):
  multipleimages = MultipleImages.objects.get(id = multi_id)
  multipleimages.delete()
  return redirect('multiple_image_management')


# REVIEW MANAGMENT
@never_cache
@login_required(login_url='signin')
def review_management(request):
  reviews = ReviewRating.objects.all()
  context = {
    'reviews': reviews
  }
  return render(request, 'manager/review_management.html', context)

#BLOCK REVIEW
@never_cache
@login_required(login_url='signin')
def review_block(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status = False
  review.save()
  return redirect('review_management')

# UNBLOCK REVIEW
@never_cache
@login_required(login_url='signin')
def review_unblock(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status= True
  review.save()
  return redirect('review_management') 

 