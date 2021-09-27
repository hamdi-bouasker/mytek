from django.contrib import admin
from .models import Payment, Order, OrderProduct 


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product_price', 'quantity', 'ordered')
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'tel', 'thecountry', 'order_number', 'order_total', 'tax', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'f_name', 'l_name', 'email', 'tel']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
