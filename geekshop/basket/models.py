from django.db import models
from users.models import User
from products.models import Product


# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Basket for {self.user} | Product {self.product}'

    def get_subtotal(self):
        return self.product.price * self.quantity

    @classmethod
    def get_total_sum(cls, user):
        total = 0
        for basket_product in cls.objects.filter(user=user):
            total += basket_product.get_subtotal()
        return total

    @classmethod
    def get_total_quantity(cls, user):
        total = 0
        for basket_product in cls.objects.filter(user=user):
            total += basket_product.quantity
        return total
