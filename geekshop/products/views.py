import datetime
import quopri

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from djmoney.money import Money

from django.shortcuts import render
import json
import os
import pathlib
from products.models import Product, ProductCategory

app_path = pathlib.Path(__file__).resolve().parent


# Create your views here.
def index(request):
    context = {'title': 'Geekshop - main'}
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_id=1):
    with open(os.path.join(app_path, 'fixtures/slides.json')) as file:
        slides_paths = json.load(file)

    if category_id:
        products = Product.objects.filter(category_id=category_id).select_related('category')
    else:
        products = Product.objects.all().select_related('category')

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
        'categories': ProductCategory.objects.all()
    }

    return render(request, 'products/products.html', context)


def get_product_price_json(request, pk):
    price = Product.objects.get(pk=pk).price or 0
    return JsonResponse({'price': price})
