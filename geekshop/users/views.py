from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse

from users.forms import UserLoginForm, UserRegisterForm


# Create your views here.
def login(request):
    form = UserLoginForm()
    errors = {}

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            errors = form.errors.as_data()

    context = {
        'title': 'Geekshop login',
        'form': form,
        'errors': errors
    }
    return render(request, 'users/login.html', context)


def register(request):
    form = UserRegisterForm()
    errors = {}

    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users_app:login'))
        else:
            errors = form.errors.as_data()

    context = {
        'title': 'Geekshop register',
        'form': form,
        'errors': errors
    }
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
