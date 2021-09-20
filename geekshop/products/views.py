import datetime
import quopri

from djmoney.money import Money

from django.shortcuts import render
import json
import os
import pathlib

app_path = pathlib.Path(__file__).resolve().parent


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


def products(request):
    with open(os.path.join(app_path, 'fixtures/slides.json')) as file:
        slides_paths = json.load(file)

    with open(os.path.join(app_path, 'fixtures/products_description.json'), encoding='utf-8') as file:
        products = json.load(file)

    context = {
        'slides': slides_paths,
        'products': products
    }

    return render(request, 'products/products.html', context)
