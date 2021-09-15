import datetime
from djmoney.money import Money

from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'products/index.html')


def products(request):
    return render(request, 'products/products.html')


def test(request):
    context = {
        'title': 'geekshop',
        'header': 'Welcome to our website!',
        'user': 'Pablo',
        'time': datetime.datetime.now(),
        'products': [
            {'id': 1,
             'name': 'Худи черного цвета с монограммами adidas Originals',
             'price': Money(6090.20, 'RUB')
             },
            {'id': 2,
             'name': 'Синяя куртка The North Face',
             'price': Money(23725.50, 'RUB')
             },
        ],
        'promo_products': [
            {'id': 1,
             'name': 'Snickers Nike',
             'price': Money(990, 'RUB')
             },
            {'id': 2,
             'name': 'T-shirt ABIBAS',
             'price': Money(990, 'RUB')
             }
        ]
    }
    return render(request, 'products/test.html', context=context)
