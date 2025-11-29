# services/models.py

from django.db import models
from django.conf import settings # Best practice for referencing AUTH_USER_MODEL
from django.urls import reverse
import uuid # For unique, readable URLs/slugs
from django.db.models import Avg

# 1. Service Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# 2. Service Listing
class Service(models.Model):
    # Foreign Key (Relational Design)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_seller': True}, # Only allow sellers
        related_name='services'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='services'
    )

    # Core Fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Media File Upload
    cover_image = models.ImageField(
        upload_to='service_images/%Y/%m/%d/',
        default='service_images/default_service.jpg'
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Use slug in the URL for better SEO and readability
        return reverse('service_detail', kwargs={'slug': self.slug})

    # Helper method for average rating (will be implemented with 'reviews' app)
    @property
    def average_rating(self):
        """Calculates the average rating based on all associated reviews."""
        # Check if the 'reviews' app is loaded and the Review model is accessible
        if hasattr(self, 'reviews'):
            # Use the Avg aggregation function on the 'rating' field
            avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
            # Return the average, rounded to one decimal place, or None if no reviews
            return round(avg, 1) if avg is not None else None
        return None

    # ADD THIS PROPERTY (Helper for display)
    @property
    def total_reviews(self):
        """Returns the total number of reviews for the service."""
        return self.reviews.count()
        
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})