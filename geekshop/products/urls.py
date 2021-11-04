from django.urls import path
from django.views.decorators.cache import cache_page

from .views import products, get_product_price_json, ProductDetails

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('category-<int:category_id>/', products, name='category'),
    path('page-<int:page_id>/', cache_page(120)(products), name='page'),
    # path('page-<int:page_id>/', products, name='page'),
    path('price/<int:pk>/', get_product_price_json, name='get_product_price'),
    path('details/<int:pk>/', cache_page(120)(ProductDetails.as_view()), name='product_details'),
]
