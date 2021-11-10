from os import path

from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, redirect, \
    get_object_or_404
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView, View, ContextMixin
from django.views.generic.edit import FormMixin, UpdateView, ProcessFormView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from geekshop.mixin import TitleContextMixin
from geekshop.settings import LOGIN_URL
from users.models import User
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, \
    UserProfileEditForm
from basket.models import Basket


class Login(LoginView, TitleContextMixin):
    title = 'Geekshop login'
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        return super().get(request, *args, **kwargs)


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
            user = form.save()
            if user and send_verify_link(user):
                messages.success(request,
                                 'Success registration! Verification link was'
                                 ' sent to your email!')
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
    title = 'Geekshop - profile'
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users_app:profile')

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['form'] = UserProfileForm(instance=self.request.user)
        context['profile_form'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST,
                               instance=request.user,
                               files=request.FILES)
        form_edit = UserProfileEditForm(data=request.POST,
                                        instance=request.user.userprofile, )
        if form.is_valid() and form_edit.is_valid():
            form.save()
            messages.success(self.request, 'Success! Profile was changed!')
            return redirect(self.success_url)
        else:
            messages.error(self.request,
                           'Form not valid! Read the following error or get '
                           'back to admin if theres not any.')
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


def send_verify_link(user):
    site = settings.DOMAIN_NAME
    verify_path = reverse('users:verify',
                          args=[user.email, user.activation_key])
    varify_link = f'{site}{verify_path}'
    subject = f'{user.username}, activate your Geekshop account!'
    message = f'To activate your account, please follow this link:\n{varify_link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER,
                     [user.email], fail_silently=False)
    return varify_link


def verify(request, email: str, activation_key: str):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'users/verification.html')
    except Exception as e:
        print(e)
        return reverse_lazy('index')
