from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basket.models import Basket
from basket.views import get_total_sum, get_total_quantity


# Create your views here.
def login(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': 'Geekshop login',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Success! Congratulations on your registration!')
            return HttpResponseRedirect(reverse('users_app:login'))

    context = {
        'title': 'Geekshop - register',
        'form': form,
    }
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request):
    form = UserProfileForm(instance=request.user)
    basket_products = Basket.objects.filter(user=request.user)

    total_sum = get_total_sum(basket_products)
    total_quantity = get_total_quantity(basket_products)

    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users_app:profile'))

    context = {
        'title': 'Geekshop - Profile',
        'form': form,
        'basket_products': basket_products,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
    return render(request, 'users/profile.html', context)
