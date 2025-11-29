# chat/views.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .forms import MessageForm

@login_required
def send_message(request, order_pk):
    """
    Handles POST request to send a message within an order thread.
    """
    order = get_object_or_404(Order, pk=order_pk)

    # Permission check: Must be the client or seller of the order
    user = request.user
    if user != order.client and user != order.seller:
        messages.error(request, "You do not have permission to message this order.")
        return redirect('order_detail', pk=order.pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.order = order
            message.sender = user
            
            # The receiver is set automatically in the Message model's save method
            try:
                message.save()
                messages.success(request, "Message sent.")
            except ValueError as e:
                # Should not happen if models.py logic is correct, but safe to catch
                messages.error(request, f"Error sending message: {e}") 
                
            return redirect('order_detail', pk=order.pk)
    
    messages.error(request, "Invalid message content.")
    return redirect('order_detail', pk=order.pk)