from django.contrib import admin
from .models import Product, ReviewRating

class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'discount_price','stock', 'updated_at', 'is_available', 'is_trending', 'is_topSelling')
    prepopulated_fields = {'slug': ('name',), 'alt_text': ('name',)} 
    
    class Meta:
        ordering = ['category']

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
