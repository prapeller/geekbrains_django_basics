from django.db import models
from django.conf import settings

from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCESSING = 'STP'
    PAID = 'PD'
    PROCESSED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNL'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'FORMING'),
        (SENT_TO_PROCESSING, 'SENT TO PROCESS'),
        (PAID, 'PAID'),
        (PROCESSED, 'IN PROCESS'),
        (READY, 'READY'),
        (CANCEL, 'CANCELLED'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='created on', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated on', auto_now=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, verbose_name='status',
                              max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='is active', default=True)

    def __str__(self):
        return f'order id: {self.pk}, product: {list(self.order_products)}'

    def get_total_quantity(self):
        products = self.order_products.select_related()
        return sum(list(map(lambda product: product.quantity, products)))

    def get_total_price(self):
        products = self.order_products.select_related()
        return sum(list(map(lambda product: product.get_subtotal(), products)))

    def get_products(self):
        products = self.order_products.select_related()
        return products

    def delete(self, using=None, keep_parents=False):
        for product in self.order_products.select_related():
            product.quantity += product.quantity
            product.save()
        self.is_active = False
        self.save()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name='order',
                              related_name='order_products',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)

    def get_subtotal(self):
        return self.product.price * self.quantity
