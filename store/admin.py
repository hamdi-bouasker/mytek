from django.contrib import admin
from .models import Product, ProductGallery, ReviewRating
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'discount_price','stock', 'updated_at', 'is_available', 'is_trending', 'is_topSelling')
    prepopulated_fields = {'slug': ('name',), 'alt_text': ('name',)} 
    inlines = [ProductGalleryInline]
    class Meta:
        ordering = ['category']

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
