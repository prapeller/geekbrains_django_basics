from django.db import models
from django.conf import settings
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse

from basket.models import Basket
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
        return f'Order id: {self.pk} from {self.created}, last update {self.updated}'

    def get_absolute_url(self):
        return reverse('orders_app:order_list')

    def get_total_quantity(self):
        ord_products = self.order_products.select_related()
        return sum(list(map(lambda ord_product: ord_product.quantity, ord_products)))

    def get_total_price(self):
        ord_products = self.order_products.select_related()
        return sum(list(map(lambda ord_product: ord_product.get_subtotal(), ord_products)))

    def get_products(self):
        order_products = self.order_products.select_related()
        return order_products

    def delete(self, using=None, keep_parents=False):
        ord_products = self.order_products.select_related()
        for ord_product in ord_products:
            ord_product.product.quantity += ord_product.quantity
            ord_product.product.save()
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

    @classmethod
    def get_quantity(cls, pk):
        return cls.objects.get(pk=pk).quantity


# @receiver(pre_delete, sender=Basket)
# @receiver(pre_delete, sender=OrderProduct)
# def product_quantity_update_delete(sender, instance, **kwargs):
#     instance.product.quantity += instance.quantity
#     instance.save()
#
#
# @receiver(pre_save, sender=Basket)
# @receiver(pre_save, sender=OrderProduct)
# def product_quantity_update_save(sender, instance, **kwargs):
#     if not instance.pk:
#         instance.product.quantity -= instance.quantity
#     else:
#         instance.product.quantity -= instance.quantity - Basket.get_quantity(instance.pk)
#     instance.product.save()
