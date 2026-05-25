from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Управление категориями (только для админа)
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:product_id>/', views.add_to_favorites, name='toggle_favorite'),
    
    
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart'),
    path('register/', views.register, name='register'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart_view, name='cart_view'),
]