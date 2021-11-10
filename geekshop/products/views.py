import datetime
import quopri

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.cache import cache_page, never_cache
from django.views.generic import DetailView
from djmoney.money import Money

from django.shortcuts import render, get_object_or_404
import json
import os
import pathlib
from products.models import Product, ProductCategory

app_path = pathlib.Path(__file__).resolve().parent

PRODUCTS = 'products'
CATEGORIES = 'product_categories'


def index(request):
    context = {'title': 'Geekshop - main'}
    return render(request, 'products/index.html', context)


def get_cached_queryset(key, model, pk=None):
    if settings.LOW_CACHE:
        key = key if not pk else f'{key}_{pk}'
        cached_val = cache.get(key)

        if not cached_val:
            cached_val = model.objects.all() if not pk else get_object_or_404(model, pk=pk)
            cache.set(key, cached_val)
        return cached_val
    else:
        return model.objects.all() if not pk else get_object_or_404(model, pk=pk)


# всю вьюху лучше тут не кэшить, иначе после логина шапка не будет меняться
# @cache_page(60 * 3)
def products(request, category_id=None, page_id=1):
    with open(os.path.join(app_path, 'fixtures/slides.json')) as file:
        slides_paths = json.load(file)

    if category_id:
        products = get_cached_queryset(PRODUCTS, Product).filter(
            category_id=category_id).order_by('pk').select_related('category')
    else:
        products = get_cached_queryset(PRODUCTS, Product).order_by('pk').select_related('category')

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'Geekshop - catalog',
        'slides': slides_paths,
        'products': products_paginator,
        'categories': get_cached_queryset(CATEGORIES, ProductCategory)
    }

    return render(request, 'products/products.html', context)


class ProductDetails(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_cached_queryset(key=PRODUCTS, model=Product,
                                                 pk=self.kwargs.get('pk'))
        context['categories'] = get_cached_queryset(CATEGORIES, ProductCategory)
        return context


# @never_cache
@cache_page(60 * 3)
def get_product_price_json(request, pk):
    # price = Product.objects.get(pk=pk).price or 0
    price = get_cached_queryset(key=PRODUCTS, model=Product, pk=pk).price or 0
    return JsonResponse({'price': price})
