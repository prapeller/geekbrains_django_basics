from django.urls import path
from admins.views import index, UserCreateView, UserListView, UserUpdateView, ActDeact, \
    UserDeleteView, MakeStuff, ProductCreateView, ProductListView, ProductUpdateView, \
    ProductDeleteView, CategoryCreate, CategoryList, CategoryUpdate, CategoryDelete

app_name = 'admins_app'

urlpatterns = [
    path('', index, name='index'),
    path('user-create/', UserCreateView.as_view(), name='user_create'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user-act-deact/<int:pk>/', ActDeact.as_view(), name='user_act_deact'),
    path('user-stuffize/<int:pk>/', MakeStuff.as_view(), name='user_stuffize'),

    path('product-create/', ProductCreateView.as_view(), name='product_create'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('product-update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product-delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('category-create/', CategoryCreate.as_view(), name='category_create'),
    path('category-list/', CategoryList.as_view(), name='category_list'),
    path('category-update/<int:pk>/', CategoryUpdate.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', CategoryDelete.as_view(), name='category_delete'),
]
