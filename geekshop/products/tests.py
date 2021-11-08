from django.test import TestCase
from django.test.client import Client

from products.models import ProductCategory, Product

SUCCESS_STATUS_CODE = 200
REDIRECT_STATUS_CODE = 302


class TestMainSmokeTest(TestCase):

    def setUp(self) -> None:
        """preinstalled parameters"""
        category = ProductCategory.objects.create(name='Test')
        self.prod_1 = Product.objects.create(category=category, name='test_product', price=100)
        self.prod_2 = Product.objects.create(category=category, name='test_product1', price=10)
        self.client = Client()

    def test_products_page(self):
        """
        testing to open page
        /products/
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, SUCCESS_STATUS_CODE)

    def test_products_product(self):
        """
        test to open page
        /products/details/<int:pk>
        """
        for product in Product.objects.all():
            resp = self.client.get(f'/products/details/{product.pk}/')
            self.assertEqual(resp.status_code, SUCCESS_STATUS_CODE)

    def test_products_basket(self):
        """
        test to open page and redirect if not logged in
        /products/details/<int:pk>
        """
        resp = self.client.get('/users/profile/')
        self.assertEqual(resp.status_code, REDIRECT_STATUS_CODE)

    def tearDown(self) -> None:
        self.prod_1.delete()
        self.prod_2.delete()


