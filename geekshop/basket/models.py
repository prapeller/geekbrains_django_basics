from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self):
        for basket_product in self:
            basket_product.product.quantity += basket_product.quantity
            basket_product.product.save()
        super().delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'user: {self.user} | product: {self.product}'

    def get_subtotal(self):
        return self.product.price * self.quantity

    @cached_property
    def get_cached(self):
        return self.user.basket.select_related()

    def get_total_sum(self):
        return sum(basket_product.get_subtotal() for basket_product in self.get_cached)

    def get_total_quantity(self):
        return sum(basket_product.quantity for basket_product in self.get_cached)

    @classmethod
    def get_quantity(cls, pk):
        return cls.objects.get(pk=pk).quantity

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.product.quantity -= self.quantity
        else:
            self.product.quantity -= self.quantity - Basket.get_quantity(self.pk)
        self.product.save()
        super().save()

