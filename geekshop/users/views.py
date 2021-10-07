from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View, ContextMixin
from django.views.generic.edit import FormMixin, UpdateView, ProcessFormView

from geekshop.mixin import TitleContextMixin
from geekshop.settings import LOGIN_URL
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basket.models import Basket


# Create your views here.

class Login(LoginView, TitleContextMixin):
    title = 'Geekshop login'
    form_class = UserLoginForm
    template_name = 'users/login.html'


# def login(request):
#     form = UserLoginForm()
#
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#             return HttpResponseRedirect(reverse('index'))
#
#     context = {
#         'title': 'Geekshop login',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


class Register(TemplateView, FormMixin, TitleContextMixin):
    title = 'Geekshop - register'
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users_app:login')

    def post(self, request):
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Success! Congratulations on your registration!')
            return HttpResponseRedirect(reverse('users_app:login'))
        return HttpResponseRedirect(reverse('users_app:register'))


# def register(request):
#     form = UserRegisterForm()
#
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Success! Congratulations on your registration!')
#             return HttpResponseRedirect(reverse('users_app:login'))
#
#     context = {
#         'title': 'Geekshop - register',
#         'form': form,
#     }
#     return render(request, 'users/register.html', context)


class Logout(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(LOGIN_URL)


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

@method_decorator(user_passes_test(lambda u: u.is_authenticated), name='dispatch')
class Profile(TemplateView, FormMixin, TitleContextMixin):
    title = 'Geekshop - register'
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users_app:profile')

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['basket_products'] = Basket.objects.filter(user=self.request.user)
        context['form'] = UserProfileForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=self.request.POST, instance=self.request.user, files=self.request.FILES)
        if form.is_valid():
            messages.success(self.request, 'Success! Profile was changed!')
            form.save()
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Form not valid! Read the following error or get back to admin if theres not any.')
            return redirect(self.success_url)

# @login_required
# def profile(request):
#     form = UserProfileForm(instance=request.user)
#     basket_products = Basket.objects.filter(user=request.user)
#
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             messages.success(request, 'Success! Profile was changed!')
#             form.save()
#             return HttpResponseRedirect(reverse('users_app:profile'))
#         else:
#             messages.error(request, 'Form not valid! Read the following error or get back to admin if theres not any.')
#
#     context = {
#         'title': 'Geekshop - Profile',
#         'form': form,
#         'basket_products': basket_products,
#     }
#     return render(request, 'users/profile.html', context)
