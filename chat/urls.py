# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Submit a message (via POST)
    path('<int:order_pk>/send/', views.send_message, name='send_message'),
]