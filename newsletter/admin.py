from django.contrib import admin
from .models import Subscribe, Contact


class SubscribeAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'title', 'body', 'created_at')
    
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('email', 'created_at')
  
admin.site.register(SubscribeAdmin, Subscribe)
admin.site.register(ContactAdmin, Contact)
