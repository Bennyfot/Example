import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='gte', label='Цена от')
    max_price = django_filters.NumberFilter(field_name='final_price', lookup_expr='lte', label='Цена до')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), empty_label='Все категории')
    in_stock = django_filters.BooleanFilter(field_name='stock', method='filter_in_stock', label='Только в наличии')

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']