from django.urls import path
from admins.views import index, UserCreateView, UserListView, UserUpdateView, ActDeact, UserDeleteView, MakeStuff

app_name = 'admins_app'

urlpatterns = [
    path('', index, name='index'),
    path('user-create/', UserCreateView.as_view(), name='user_create'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user-act-deact/<int:pk>/', ActDeact.as_view(), name='user_act_deact'),
    path('user-stuffize/<int:pk>/', MakeStuff.as_view(), name='user_stuffize'),
]


