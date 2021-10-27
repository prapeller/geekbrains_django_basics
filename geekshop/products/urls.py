from django.urls import path
from .views import products, get_product_price_json

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('category-<int:category_id>/', products, name='category'),
    path('page-<int:page_id>/', products, name='page'),
    path('price/<int:pk>/', get_product_price_json, name='get_product_price'),
]
