# reviews/models.py

from django.db import models
from django.conf import settings
from services.models import Service
from orders.models import Order
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    # Foreign Keys
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Keep the review if the client deletes their account
        null=True, 
        limit_choices_to={'is_client': True}
    )
    # Crucial link: Ensures one review per completed order
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        related_name='review'
    )

    # Core Fields
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)] # Rating from 1 to 5
    )
    comment = models.TextField(max_length=500, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        # The (service, client) constraint is usually used, but (order) is more specific here.
        # unique_together = ('service', 'client') # Ensures a client can only review a service once (optional)

    def __str__(self):
        return f"{self.rating}/5 for {self.service.title} by {self.client.username}"