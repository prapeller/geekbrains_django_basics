from django import template
from basket.models import Basket

register = template.Library()


@register.filter(name='get_total_quantity')
def get_total_quantity(user):
    return Basket.get_total_quantity(user)


@register.filter(name='get_total_sum')
def get_total_sum(user):
    return Basket.get_total_sum(user)
