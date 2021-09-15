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
            'vendor/img/slides/slide-3.jpg',
            'vendor/img/slides/slide-4.jpg',
        ],
        'products': [
            {
                'card_title': 'Худи черного цвета с монограммами adidas Originals',
                'price': Money(6090, 'RUB'),
                'card_text': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
                'image': 'vendor/img/products/Adidas-hoodie.png'
            },
            {
                'card_title': 'Синяя куртка The North Face',
                'price': Money(23725, 'RUB'),
                'card_text': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.',
                'image': 'vendor/img/products/Blue-jacket-The-North-Face.png'
            },
            {
                'card_title': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                'price': Money(3390, 'RUB'),
                'card_text': 'Материал с плюшевой текстурой. Удобный и мягкий.',
                'image': 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png'
            },
            {
                'card_title': 'Черный рюкзак Nike Heritage',
                'price': Money(2340, 'RUB'),
                'card_text': 'Плотная ткань. Легкий материал.',
                'image': 'vendor/img/products/Black-Nike-Heritage-backpack.png'
            },
            {
                'card_title': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                'price': Money(13590, 'RUB'),
                'card_text': 'Гладкий кожаный верх. Натуральный материал.',
                'image': 'vendor/img/products/Black-Dr-Martens-shoes.png'
            },
            {
                'card_title': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                'price': Money(2890, 'RUB'),
                'card_text': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
                'image': 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png'
            },
        ]
    }

    return render(request, 'products/products.html', context)
