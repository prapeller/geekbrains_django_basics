from django.urls import path
from django.views.decorators.cache import cache_page

from .views import products, get_product_price_json, ProductDetails

app_name = 'products'

urlpatterns = [
    path('', products, name='main'),
    path('category-<int:category_id>/', products, name='category'),

    # cache_page(...)(view) для FBV не работает
    # path('page-<int:page_id>/', cache_page(180)(products), name='page'),

    # FBV работает только если задекорировать view
    path('page-<int:page_id>/', products, name='page'),

    path('price/<int:pk>/', get_product_price_json, name='get_product_price'),

    # cache_page(...)(class.as_view()) для CBV работает
    path('details/<int:pk>/', cache_page(60 * 3)(ProductDetails.as_view()), name='product_details'),
]
