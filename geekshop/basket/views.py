from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse

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


@login_required
def edit_qty(request, id, qty):
    if request.is_ajax():
        basket_product = Basket.objects.get(id=id)
        if qty > 0:
            basket_product.quantity = qty
            basket_product.save()
        else:
            basket_product.delete()

        basket_products = Basket.objects.filter(user=request.user)
        context = {
            'basket_products': basket_products
        }
        result = render_to_string('basket/basket.html', context)
        return JsonResponse({'result': result})
