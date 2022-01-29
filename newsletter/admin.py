from django.contrib import admin
from .models import Subscribe, Contact


class SubscribeAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'created_at')
    
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'created_at')
  
admin.site.register(Subscribe,SubscribeAdmin)
admin.site.register(Contact,ContactAdmin)
