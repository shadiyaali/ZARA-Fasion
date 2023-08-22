from django.urls import path
from . import views


urlpatterns = [
    
    path('wishlist/add-to-wishlist',views.add_to_wishlist, name="add_to_wishlist"),
    path('delete-from-wishlist/<int:id>',views.delete_from_wishlist, name="delete_from_wishlist"),
    path('wishlist/',views.wishlist, name="wishlist"),
    path('addt-o-wishlist/<int:id>',views.add_to_wishlist,name='add_to_wishlist')

    # path('checkout/', views.checkout, name='checkout'),

]