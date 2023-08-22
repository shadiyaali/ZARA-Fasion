from django.contrib import admin
from .models import Product,Variation,ReviewRating
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
      list_display = ('product', 'variation_category', 'variation_value', 'is_active')
      list_editable = ('is_active',)
      list_filter = ('product', 'variation_category', 'variation_value')

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user','subject','rating','created_at',)
 
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(MultipleImages)
admin.site.register(Profile)
admin.site.register(ReviewRating,ReviewRatingAdmin)