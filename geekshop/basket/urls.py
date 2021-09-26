from django.urls import path
from basket.views import add_product, remove_product

app_name = 'basket'

urlpatterns = [
    path('add_product<int:product_id>/', add_product, name='add_product'),
    path('remove_product<int:basket_product_id>/', remove_product, name='remove_product'),
]
