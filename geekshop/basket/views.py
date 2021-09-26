from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from products.models import Product
from basket.models import Basket


# Create your views here.
def get_total_sum(basket_products):
    total = 0
    if basket_products:
        for basket_product in basket_products:
            product = basket_product.product
            price = product.price
            quantity = basket_product.quantity
            total += price * quantity

    return total


def get_total_quantity(basket_products):
    total = 0
    if basket_products:
        for basket_product in basket_products:
            total += basket_product.quantity

    return total


def add_product(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    basket_products = Basket.objects.filter(user=user, product=product)

    if not basket_products:
        Basket.objects.create(user=user, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    basket_product = basket_products[0]
    basket_product.quantity += 1
    basket_product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product(request, basket_product_id):
    Basket.objects.filter(id=basket_product_id).first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
