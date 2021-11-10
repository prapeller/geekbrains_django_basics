from django.test import TestCase
from django.test.client import Client

from products.models import ProductCategory, Product

STATUS_CODE_SUCCESS = 200
STATUS_CODE_REDIRECT = 302


class TestMainSmokeTest(TestCase):

    def setUp(self) -> None:
        """preinstalled ProductCategory and Product instances"""
        category = ProductCategory.objects.create(name='Test')
        self.prod_1 = Product.objects.create(category=category, name='test_product', price=100,
                                             image='product_images/Adidas-hoodie.png')
        self.prod_2 = Product.objects.create(category=category, name='test_product1', price=10,
                                             image='product_images/Adidas-hoodie.png')
        self.client = Client()

    def test_products_page(self):
        """
        testing to open page
        /products/
        """
        resp = self.client.get('/products/')
        self.assertEqual(resp.status_code, STATUS_CODE_SUCCESS)

    def test_products_details(self):
        """
        test to open page
        /products/details/<int:pk>
        """
        for product in Product.objects.all():
            resp = self.client.get(f'/products/details/{product.pk}/')
            self.assertEqual(resp.status_code, STATUS_CODE_SUCCESS)

    def test_users_profile(self):
        """
        test to open page and redirect if not logged in
        /users/profile/
        """
        resp = self.client.get('/users/profile/')
        self.assertEqual(resp.status_code, STATUS_CODE_REDIRECT)

    def tearDown(self) -> None:
        self.prod_1.delete()
        self.prod_2.delete()
