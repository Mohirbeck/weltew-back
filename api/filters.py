from django_filters import rest_framework as filters
from .models import ProductModel, ProductCategoryModel, CollectionModel, CollectionCategoryModel, CartModel, Customer


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    price_min = filters.NumberFilter(lookup_expr='gte')
    price_max = filters.NumberFilter(lookup_expr='lte')
    category = filters.ModelChoiceFilter(
        queryset=ProductCategoryModel.objects.all())

    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'availibility',
                  'category', 'price_min', 'price_max']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].label = "Категория"
        self.filters['price_min'].label = "Цена от"
        self.filters['price_max'].label = "Цена до"
        self.filters['availibility'].label = "Наличие"
        self.filters['name'].label = "Название"
        self.filters['description'].label = "Описание"


class CollectionFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    category = filters.ModelChoiceFilter(
        queryset=CollectionCategoryModel.objects.all())

    class Meta:
        model = CollectionModel
        fields = ['name', 'description', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].label = "Категория"
        self.filters['name'].label = "Название"
        self.filters['description'].label = "Описание"

class CartFilter(filters.FilterSet):
    customer = filters.ModelChoiceFilter(
        queryset=Customer.objects.all())

    class Meta:
        model = CartModel
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['customer'].label = "Покупатель"