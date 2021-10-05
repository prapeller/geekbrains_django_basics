from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm
from geekshop.mixin import IsSuperuserDispatchMixin, IsStuffDispatchMixin
from products.models import Product
from users.models import User


@login_required
def index(request):
    context = {
        'title': 'GeekShop - Admin',
    }

    return render(request, 'admins/admin.html', context)


# @method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class UserListView(ListView, IsStuffDispatchMixin):
    model = User
    template_name = 'admins/admin-users-list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | User list'
        return context


# @method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class UserCreateView(CreateView, IsStuffDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins_app:user_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | Create User'
        return context


# @method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class UserUpdateView(UpdateView, IsStuffDispatchMixin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'image']
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins_app:user_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | Update User'
        return context


# @method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UserDeleteView(DeleteView, IsSuperuserDispatchMixin):
    model = User
    template_name = 'admins/admin-users-list.html'
    success_url = reverse_lazy('admins_app:user_list')


# @method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class ActDeact(DeleteView, IsStuffDispatchMixin):
    model = User
    template_name = 'admins/admin-users-list.html'
    success_url = reverse_lazy('admins_app:user_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False if self.object.is_active else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class MakeStuff(DeleteView, IsSuperuserDispatchMixin):
    model = User
    template_name = 'admins/admin-users-list.html'
    success_url = reverse_lazy('admins_app:user_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_staff = False if self.object.is_staff and not self.object.is_superuser else True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductCreateView(CreateView, IsStuffDispatchMixin):
    model = Product
    fields = ('name', 'description', 'price', 'quantity', 'category')
    template_name = 'admins/admin-products-create.html'
    success_url = reverse_lazy('admins_app:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | Create Product'
        return context


class ProductListView(ListView, IsStuffDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | Product list'
        return context


class ProductUpdateView(UpdateView, IsStuffDispatchMixin):
    model = Product
    fields = ['name', 'description', 'price', 'quantity', 'category']
    template_name = 'admins/admin-products-update-delete.html'
    success_url = reverse_lazy('admins_app:product_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Admin panel | Update Product'
        return context


class ProductDeleteView(DeleteView, IsSuperuserDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-list.html'
    success_url = reverse_lazy('admins_app:product_list')