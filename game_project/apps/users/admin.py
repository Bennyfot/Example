from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rating', 'games_played', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Игровая статистика', {'fields': ('rating', 'games_played')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)