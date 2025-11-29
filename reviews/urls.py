# reviews/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Submit a review for a specific completed order
    path('create/<int:order_pk>/', views.ReviewCreateView.as_view(), name='create_review'),
]