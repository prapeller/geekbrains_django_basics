from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from products.models import Product
from basket.models import Basket
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
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


@login_required
def remove_product(request, basket_product_id):
    Basket.objects.filter(id=basket_product_id).first().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
