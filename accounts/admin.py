from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _

from .models import User, Client, Manager


class UserAdmin(DefaultUserAdmin):
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user', 'manager',
                                         'passport_number')}),
        (_('Status'), {'fields': ('is_active',)}),
    )
    list_display = ('id', 'user', 'is_active')

admin.site.register(Client, ClientAdmin)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Manager, ManagerAdmin)
