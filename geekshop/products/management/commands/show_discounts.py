from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Q, F, When, Case, DecimalField, CharField
from prettytable import PrettyTable

from ordersapp.models import OrderProduct


class Command(BaseCommand):
    def handle(self, *args, **options):
        DISCOUNT_1 = 0.3
        DISCOUNT_2 = 0.15
        DISCOUNT_3 = 0.05

        disc_1_condition = Q(order__is_active=True) & Q(order__updated__lte=F('order__created') + timedelta(hours=12))
        disc_3_condition = Q(order__is_active=True) & Q(order__updated__gt=F('order__created') + timedelta(days=1))
        disc_2_condition = Q(order__is_active=True) & Q(~disc_1_condition & ~disc_3_condition)

        when_disc_1 = When(disc_1_condition, then=DISCOUNT_1)
        when_disc_2 = When(disc_2_condition, then=DISCOUNT_2)
        when_disc_3 = When(disc_3_condition, then=DISCOUNT_3)

        when_subtotal_with_disc_1 = When(disc_1_condition, then=F('product__price') * F('quantity') * (1 - DISCOUNT_1))
        when_subtotal_with_disc_2 = When(disc_2_condition, then=F('product__price') * F('quantity') * (1 - DISCOUNT_2))
        when_subtotal_with_disc_3 = When(disc_3_condition, then=F('product__price') * F('quantity') * (1 - DISCOUNT_3))

        order_products_annotated = OrderProduct.objects.annotate(
            discount=Case(
                when_disc_1,
                when_disc_2,
                when_disc_3,
                output_field=CharField()
            )).annotate(
            subtotal_with_disc=Case(
                when_subtotal_with_disc_1,
                when_subtotal_with_disc_2,
                when_subtotal_with_disc_3,
                output_field=DecimalField()
            )).order_by('order__user', 'discount').select_related()

        table = PrettyTable([
            'User',
            'OrderId',
            'OrderIsActive',
            'Product',
            'Quantity',
            'Subtotal',
            'Discount',
            'SubtotalWithDiscount',
            'OrderDelay',
        ])
        table.align = 'r'

        for op in order_products_annotated:
            table.add_row([
                op.order.user,
                op.order.id,
                op.order.is_active,
                op.product,
                op.quantity,
                op.get_subtotal(),
                f'{(op.discount * 100):.0f} %' if op.discount else '-',
                op.subtotal_with_disc,
                op.order.updated - op.order.created,
            ])

        print(table)
