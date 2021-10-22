from django.http import HttpResponseRedirect

from basket.models import Basket
from ordersapp.forms import OrderProductForm
from ordersapp.models import Order, OrderProduct
from geekshop.mixin import TitleContextMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory, modelformset_factory
from django.db import transaction


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView, TitleContextMixin):
    model = Order
    title = 'Geekshop | Create Order'
    fields = []
    template_name_suffix = '_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ord_products = Basket.objects.filter(user=self.request.user)
        OrdProdFormSet = inlineformset_factory(Order, OrderProduct, form=OrderProductForm,
                                               extra=ord_products.count())
        formset = OrdProdFormSet()
        if self.request.POST:
            formset = OrdProdFormSet(self.request.POST)

        for i, form in enumerate(formset.forms):
            product = ord_products[i].product
            quantity = Basket.objects.filter(product_id=product.id,
                                             user_id=self.request.user.id).first().quantity
            price = product.price

            form.initial['product'] = product
            form.initial['quantity'] = quantity
            form.initial['price'] = price

        context['formset'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        if self.object.get_total_quantity() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView, TitleContextMixin):
    model = Order
    title = 'Geekshop | Update Order'
    fields = []
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrdProdFormSet = inlineformset_factory(Order, OrderProduct, form=OrderProductForm, extra=1)
        formset = OrdProdFormSet(instance=self.object)
        if self.request.POST:
            formset = OrdProdFormSet(self.request.POST, instance=self.object)

        for form in formset.forms:
            if form.instance.pk:
                form.initial['price'] = form.instance.product.price

        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            # form.instance.user = self.request.user
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        if self.object.get_total_quantity() == 0:
            self.object.delete()

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders_app:order_list')


class OrderDetail(DetailView, TitleContextMixin):
    model = Order
    title = 'Geekshop | Order Details'


def order_send_to_process(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCESSING
    order.save()
    return HttpResponseRedirect(reverse('orders_app:order_list'))
