from django.urls import path
from .views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('category-<int:category_id>/', products, name='category'),
    path('page-<int:page_id>/', products, name='page'),
]
