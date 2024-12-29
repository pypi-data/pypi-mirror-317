from django.contrib import admin
from .models import Role, AccessLevel


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_key')
    search_fields = ('name', 'role_key')


@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'access_key')
    search_fields = ('name', 'access_key')
