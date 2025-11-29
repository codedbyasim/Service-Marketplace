# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Order Workflow
    path('create/<slug:service_slug>/', views.create_order, name='create_order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/status/update/', views.update_order_status, name='update_order_status'),

    # Dashboard Lists
    path('client/', views.ClientOrderListView.as_view(), name='client_orders'),
    path('seller/', views.SellerOrderListView.as_view(), name='seller_orders'),
]