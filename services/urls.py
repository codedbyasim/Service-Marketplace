# services/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Client Facing
    path('', views.ServiceListView.as_view(), name='home'), # Home Page
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    
    # Seller CRUD (Create, Read, Update, Delete)
    path('seller/services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('seller/services/<slug:slug>/edit/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('seller/services/<slug:slug>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('seller/my-services/', views.MyServicesListView.as_view(), name='my_services'),
    
    # Setup/Testing (Remove in production)
    path('setup/categories/', views.create_initial_categories, name='setup_categories'),
]