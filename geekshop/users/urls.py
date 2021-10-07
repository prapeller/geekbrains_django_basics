from django.urls import path
# from .views import login, logout, register, profile
from .views import Login, Logout, Register, Profile

app_name = 'users'

urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', Login.as_view(), name='login'),

    # path('register/', register, name='register'),
    path('register/', Register.as_view(), name='register'),

    # path('profile/', profile, name='profile'),
    path('profile/', Profile.as_view(template_name='users/profile.html'), name='profile'),

    # path('logout/', logout, name='logout'),
    path('logout/', Logout.as_view(), name='logout'),
]
