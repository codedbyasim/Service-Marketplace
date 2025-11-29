# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth Views
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Using built-in for simplicity
    
    # Registration Views
    path('register/client/', views.ClientRegisterView.as_view(), name='client_register'),
    path('register/seller/', views.SellerRegisterView.as_view(), name='seller_register'),
    
    # Dashboard & Profile
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_update'),
]