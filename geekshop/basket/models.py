from django.db import models
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

    @classmethod
    def get_quantity(cls, pk):
        return cls.objects.get(pk=pk).quantity

    @classmethod
    def delete_by_user(cls, user):
        cls.objects.filter(user=user).delete()

    def delete(self, using=None, keep_parents=False):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.pk:
            self.product.quantity -= self.quantity
        else:
            self.product.quantity -= self.quantity - Basket.get_quantity(self.pk)
        self.product.save()
        super().save()
