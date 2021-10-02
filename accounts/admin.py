from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile


class AccountAdmin(UserAdmin):
    list_display = ('f_name', 'l_name', 'email', 'tel', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'f_name', 'l_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')



admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, UserProfileAdmin)
