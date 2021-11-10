from django.core.management import BaseCommand
from django.db import connection

from os import path
from products.models import Product, ProductCategory

import json

JSON_PATH = 'products/fixtures'


def load_from_json(file_name):
    with open(path.join(JSON_PATH, file_name), 'r', encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cur = connection.cursor()
        cur.execute("""
        TRUNCATE products_productcategory CASCADE;
        TRUNCATE products_product CASCADE;
        """)

        products = load_from_json('product_with_djmoney.json')
        categories = load_from_json('product_category.json')

        for cat in categories:
            category_inst = cat.get('fields')
            category_inst['id'] = cat.get('pk')
            ProductCategory.objects.create(**category_inst)

        for prod in products:
            product_inst = prod.get('fields')
            product_inst['id'] = prod.get('pk')
            category_inst = ProductCategory.objects.get(id=product_inst['category'])
            product_inst['category'] = category_inst
            Product.objects.create(**product_inst)
