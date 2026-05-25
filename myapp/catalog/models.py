from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    # Основные поля
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    # Числовые поля
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    # Булево поле
    is_available = models.BooleanField(default=True)
    # Дата/время
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Изображение (для демонстрации)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    # Связи
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    # Многие-ко-многим: избранное (пользователи, которые добавили товар в избранное)
    favorites = models.ManyToManyField(User, related_name='favorite_products', blank=True)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Цена с учетом скидки"""
        return self.price * (100 - self.discount) / 100

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ('user', 'product')  # один товар в корзине один раз

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

    def get_total(self):
        return self.quantity * self.product.final_price

# Дополнительная модель для примера связи один-к-одному (профиль пользователя)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"