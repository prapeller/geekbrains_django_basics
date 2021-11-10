from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q

from admins.views import print_queries
from products.models import Product, ProductCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = list(map(lambda x: x.name, ProductCategory.objects.all()))
        print(f'all categories: {categories}')
        # products_qrst = Product.objects.filter(Q(quantity__gt=10) & Q(category__name='Accessories'))
        # products_qrst = Product.objects.filter(Q(quantity__gt=10) | Q(category__name='Accessories'))
        products_qrst = Product.objects.filter(Q(quantity__gt=10) & ~Q(category__name='Accessories'))
        for product in products_qrst:
            print(product)
        print_queries(connection.queries)
