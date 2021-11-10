from django.urls import path
from basket.views import add_product, remove_product, edit_qty

app_name = 'basket'

urlpatterns = [
    path('add_product/<int:product_id>/', add_product, name='add_product'),
    path('remove_product/<int:id>/', remove_product, name='remove_product'),
    path('edit/<int:id>/<int:qty>/', edit_qty, name='edit_qty'),
]
