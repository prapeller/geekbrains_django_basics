from django.urls import path
from .views import OrderList, OrderCreate, OrderDetail, OrderUpdate, OrderDelete, order_send_to_process

app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view(), name='order_list'),
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('detail/<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='order_delete'),
    path('send_to_process/<int:pk>/', order_send_to_process, name='order_send_to_process'),
]
