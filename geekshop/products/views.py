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
    with open(os.path.join(app_path, 'fixtu/slides.json')) as file:
        data = json.load(file)
        slides_paths = data['slides']

    with open(os.path.join(app_path, 'fixtu/products_description.json'), encoding='utf-8') as file:
        data = json.load(file)
        products_description = data['description']

    context = {
        'slides': slides_paths,
        'products': products_description
    }

    return render(request, 'products/products.html', context)
