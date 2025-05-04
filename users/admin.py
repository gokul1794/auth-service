from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'is_anonymous', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Meta', {'fields': ('is_anonymous', 'last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)
