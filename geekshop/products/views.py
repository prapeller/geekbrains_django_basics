import datetime
import quopri

from djmoney.money import Money

from django.shortcuts import render
import json
import os
import pathlib
from products.models import Product, ProductCategory

app_path = pathlib.Path(__file__).resolve().parent


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


def products(request):
    with open(os.path.join(app_path, 'fixtures/slides.json')) as file:
        slides_paths = json.load(file)

    context = {
        'slides': slides_paths,
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all()
    }

    return render(request, 'products/products.html', context)
