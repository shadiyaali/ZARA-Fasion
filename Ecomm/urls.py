 
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings 
from .import views 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('accounts' ,include('accounts.urls')),
    path('store' ,include('store.urls')),
    path('cart', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')), 
    path('orders/', include('orders.urls')), 
    path('adminpanel', include('adminpanel.urls')),
    


] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()