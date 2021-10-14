from basket.models import Basket


def basket_products(request):
    basket_products = []
    if request.user.is_authenticated:
        basket_products = Basket.objects.filter(user=request.user)
    return {'basket_products': basket_products}
