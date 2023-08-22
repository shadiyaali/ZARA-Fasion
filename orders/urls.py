
from django.urls import path
from .import views

urlpatterns = [

    path('placeorder/', views.placeorder, name = 'placeorder'), 
    path('proceed-to-pay/', views.razorpaycheck, name = 'razorpaycheck'), 
    path('myorder/', views.myorder, name='myorder'),
    path('vieworder/<str:tracking_no>/',views.vieworder, name='vieworder'),
    path('cancel-order/<str:tracking_no>/',views.cancel_order, name='cancel_order'),
    path('order-complete/',views.order_complete, name='order_complete ')

]