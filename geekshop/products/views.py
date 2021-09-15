import datetime
from djmoney.money import Money

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


def products(request):
    context = {
        'slides': [
            'vendor/img/slides/slide-1.jpg',
            'vendor/img/slides/slide-2.jpg',
            'vendor/img/slides/slide-3.jpg'
        ]
    }

    return render(request, 'products/products.html', context)
