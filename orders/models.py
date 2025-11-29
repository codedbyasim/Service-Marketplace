from django.db import models
from django.conf import settings
from services.models import Service
from django.urls import reverse
import time # Import added for time.strftime
import uuid # Import added for unique ID fallback

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Foreign Keys
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='client_orders',
        limit_choices_to={'is_client': True}
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='seller_orders',
        limit_choices_to={'is_seller': True}
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.PROTECT, # Protect service from being deleted if it has active orders
        related_name='orders'
    )

    # Core Fields
    order_ref = models.CharField(max_length=20, unique=True, editable=False)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    # Required for the private chat system (attachments TBD, add later)
    # final_delivery_file = models.FileField(upload_to='order_deliveries/%Y/%m/', blank=True, null=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_ref} ({self.service.title})"

    def save(self, *args, **kwargs):
        # 1. Ensure price_at_order is set upon creation
        # self.pk is None for a new object
        if not self.pk and not self.price_at_order:
            self.price_at_order = self.service.price
        
        # 2. Generate order_ref on creation (using a safer logic)
        if not self.order_ref:
            try:
                # Use Order (the class name) instead of the incorrect models.Order
                # Get the count of existing orders and increment for the new ID
                last_id_num = Order.objects.count()
                new_id = last_id_num + 1
                
                # Format: ORD-YYYYMMDD-NNNN
                date_part = time.strftime('%Y%m%d')
                self.order_ref = f"ORD-{date_part}-{new_id:04d}"
                
            except Exception as e:
                # Fallback in case of database issue
                self.order_ref = f'ERR-{uuid.uuid4().hex[:8].upper()}'
                print(f"Error generating Order ID: {e}")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.pk})