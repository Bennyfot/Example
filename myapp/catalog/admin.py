from django.contrib import admin
from .models import Category, Product, CartItem, Profile

# Простая регистрация всех моделей
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Profile)
