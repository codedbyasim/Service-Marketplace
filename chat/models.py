# chat/models.py

from django.db import models
from django.conf import settings
from orders.models import Order

class Message(models.Model):
    """
    Represents a single private message within an Order thread.
    """
    # Foreign Keys
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='messages' # Allows accessing messages from order.messages.all()
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    # Receiver is not strictly necessary for a 1:1 chat, but useful for integrity checks
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )

    # Core Fields
    text = models.TextField()
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in Order {self.order.order_ref}"

    def save(self, *args, **kwargs):
        # Integrity Check: Ensure sender is either client or seller of the order
        if self.sender != self.order.client and self.sender != self.order.seller:
            raise ValueError("Sender must be either the client or the seller of the order.")

        # Set the receiver automatically based on who the sender is not
        if self.sender == self.order.client:
            self.receiver = self.order.seller
        else:
            self.receiver = self.order.client
            
        super().save(*args, **kwargs)