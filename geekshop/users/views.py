from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title': 'Geekshop login'
    }
    return render(request, 'users/login.html', context)

def register(request):
    context = {
        'title': 'Geekshop register'
    }
    return render(request, 'users/register.html', context)