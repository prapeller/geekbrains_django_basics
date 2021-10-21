from basket.models import Basket
from ordersapp.forms import OrderProductForm
from ordersapp.models import Order, OrderProduct
from geekshop.mixin import TitleContextMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, \
    DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.db import transaction


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView, TitleContextMixin):
    model = Order
    title = 'Geekshop | Create Order'
    fields = []
    success_url = reverse_lazy('orders_app:order_list')
    template_name = 'ordersapp/order_create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)

        OrdProdFormSet = inlineformset_factory(Order, OrderProduct,
                                               form=OrderProductForm,
                                               extra=1)

        if self.request.POST:
            formset = OrdProdFormSet(self.request.POST)

        else:
            bskt_prod_qrst = Basket.objects.filter(user=self.request.user)

            if bskt_prod_qrst:
                OrdProdFormSet = inlineformset_factory(Order, OrderProduct,
                                                       form=OrderProductForm,
                                                       extra=bskt_prod_qrst.count())
                formset = OrdProdFormSet()

                for i, form in enumerate(formset.forms):
                    form.initial['product'] = bskt_prod_qrst[i].product
                    form.initial['quantity'] = bskt_prod_qrst[i].product.quantity
                    form.initial['price'] = bskt_prod_qrst[i].product.price

            else:
                formset = OrdProdFormSet()

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

            if self.object.get_total_price() == 0:
                self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView, TitleContextMixin):
    model = Order
    title = 'Geekshop | Update Order'
    fields = []
    success_url = reverse_lazy('orders_app:order_list')
    template_name = 'ordersapp/order_update.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)

        OrdProdFormSet = inlineformset_factory(Order, OrderProduct, form=OrderProductForm, extra=1)

        if self.request.POST:
            formset = OrdProdFormSet(self.request.POST, instance=self.object)

        else:
            formset = OrdProdFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

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

            if self.object.get_products() == 0:
                self.object.delete()

        return super(self.__class__, self).form_valid(form)


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
    return reverse_lazy('orders_app:order_list')
