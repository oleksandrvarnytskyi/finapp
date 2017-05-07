from django.contrib import admin

from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'balance', 'is_active')
    list_filter = ('is_active',)

admin.site.register(Profile, ProfileAdmin)
