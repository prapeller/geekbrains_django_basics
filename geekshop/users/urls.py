from django.urls import path
from .views import login, logout, register, profile

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
]
