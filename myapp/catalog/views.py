from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.contrib import messages
from .models import Product, CartItem, Category
from .forms import UserRegisterForm, CartItemForm, CategoryForm
from .filters import ProductFilter

def is_admin(user):
    return user.is_staff

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('catalog:product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(is_admin)
def category_list(request):
    """Список всех категорий для админа"""
    categories = Category.objects.all().order_by('name')
    
    # Поиск по категориям
    search_query = request.GET.get('search', '')
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/admin/category_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
    })

@user_passes_test(is_admin)
def category_create(request):
    """Создание новой категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect('catalog:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'catalog/admin/category_form.html', {
        'form': form,
        'title': 'Создание категории',
    })

@user_passes_test(is_admin)
def category_edit(request, pk):
    """Редактирование категории"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" успешно обновлена!')
            return redirect('catalog:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'catalog/admin/category_form.html', {
        'form': form,
        'category': category,
        'title': 'Редактирование категории',
    })

@user_passes_test(is_admin)
def category_delete(request, pk):
    """Удаление категории"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        # Проверяем, есть ли товары в этой категории
        products_count = category.products.count()
        if products_count > 0:
            messages.error(
                request, 
                f'Нельзя удалить категорию "{category_name}", так как в ней есть {products_count} товаров. '
                f'Сначала переместите или удалите товары.'
            )
        else:
            category.delete()
            messages.success(request, f'Категория "{category_name}" успешно удалена!')
        return redirect('catalog:category_list')
    
    return render(request, 'catalog/admin/category_confirm_delete.html', {
        'category': category,
    })

# catalog/views.py
def product_list(request):
    products = Product.objects.filter(is_available=True)
    
    # Применяем фильтры
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)
    
    in_stock = request.GET.get('in_stock')
    if in_stock == 'on':
        products = products.filter(stock__gt=0)
        
    sort_by = request.GET.get('sort')
    
    if sort_by == 'name':
        products = products.order_by('name')
        sort_display = 'По имени (А-Я)'
    elif sort_by == 'name_desc':
        products = products.order_by('-name')
        sort_display = 'По имени (Я-А)'
    elif sort_by == 'price_asc':
        products = products.order_by('price')
        sort_display = 'По цене (дешевые сначала)'
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
        sort_display = 'По цене (дорогие сначала)'
    elif sort_by == 'discount':
        products = products.order_by('-discount')
        sort_display = 'По скидке'
    elif sort_by == 'date':
        products = products.order_by('-created')
        sort_display = 'По новизне'
    elif sort_by == 'stock':
        products = products.order_by('-stock')
        sort_display = 'По наличию'
    else:
        # По умолчанию: сначала новые
        products = products.order_by('-created')
        sort_display = 'По новизне (по умолчанию)'
    
    # Пагинация
    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get('page', 1)  # По умолчанию страница 1
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    return render(request, 'catalog/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock == 'on',
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    # Избранное: проверяем, добавлен ли товар в избранное у текущего пользователя
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = product.favorites.filter(id=request.user.id).exists()
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
    })

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.favorites.all():
        product.favorites.remove(request.user)
    else:
        product.favorites.add(request.user)
    return redirect('catalog:product_detail', slug=product.slug)

@login_required
def favorites_list(request):
    products = request.user.favorite_products.all()
    return render(request, 'catalog/favorites.html', {'products': products})

# Корзина
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total_sum = sum(item.get_total() for item in cart_items)
    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
    return redirect('catalog:cart_view')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
    return redirect('catalog:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('catalog:cart_view')

# Пример CRUD для админа
@user_passes_test(is_admin)
def product_create(request):
    from .forms import ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})
    
@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, 'Корзина очищена')
    return redirect('catalog:cart_view')