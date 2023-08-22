from django.urls import path
from . import views 


urlpatterns = [
    path('', views.redirect_to_login),
    path('logout', views.manager_logout, name='manager_logout'),
    path('dashboard', views.manager_dashboard, name='manager_dashboard'),
    
        
    

       # USER MANAGEMENT
    path('manage_user', views.manage_user, name="manage_user"),
    path('ban_user/<int:user_id>/', views.ban_user, name='ban_user'),
    path('unban-user/<int:user_id>/', views.unban_user, name='unban_user'),


     # PRODUCT MANAGEMENT
    path('manage-product/', views.manage_product, name='manage_product'),
    path('add-product/', views.add_product, name='add_product'),  
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

      # CATEGORY MANAGEMENT 
    path('manage-category/', views.manage_category, name='manage_category'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name="delete_category"),

       
    
     #ORDER MANAGEMENT
    path('order-management/', views.order_management, name="order_management"),
    path('manager-vieworder/<str:tracking_no>/', views.manager_vieworder, name='manager_vieworder'),
    path('manager-accept_order/<str:tracking_no>/', views.manager_accept_order, name='manager_accept_order'),
    path('manager-ship_order/<str:tracking_no>/', views.manager_ship_order, name='manager_ship_order'),
    path('manager-delivered_order/<str:tracking_no>/', views.manager_delivered_order, name='manager_delivered_order'),
    path('manager-cancel_order/<str:tracking_no>/', views.manager_cancel_order, name='manager_cancel_order'),

     # VARIATION MANAGEMENT
    path('variation-management/', views.variation_management, name="variation_management"),
    path('add-variation/', views.add_variation, name='add_variation'),
    path('update-variation/<int:variation_id>/',views.update_variation,name='update_variation'),
    path('delete-variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),

     #MULTIPLE IMAGE MANAGEMENTS
    path('multiple-image_management/',views.multiple_image_management,name='multiple_image_management'),
    path('delete-multiple_images/<int:multi_id>/',views.delete_multiple_images,name='delete_multiple_images'),
    path('update-multiple_images/<int:multi_id>/',views.update_multiple_images,name='update_multiple_images'),
    path('add-multiple-images/',views.add_multiple_images,name='add_multiple_images'),


    #REVIEW MANAGER
    path('review-management/',views.review_management,name='review_management'),
    path('review-block/<int:review_id>/',views.review_block,name='review_block'),
    path('review-unblock/<int:review_id>/',views.review_unblock,name='review_unblock'),

]