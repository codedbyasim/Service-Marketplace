# orders/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .models import Order
from services.models import Service
from .forms import OrderCreationForm, OrderStatusUpdateForm
from django.utils import timezone
from chat.models import Message 
from chat.forms import MessageForm


# --- Helper Mixins ---

class OrderPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Ensures only the Client or the Seller associated with the order can view it.
    """
    def test_func(self):
        order = self.get_object()
        user = self.request.user
        return user.is_authenticated and (order.client == user or order.seller == user)

# --- Order Creation ---

@login_required
def create_order(request, service_slug):
    """
    Function-based view to handle the creation of an Order.
    Accessed from the Service Detail page.
    """
    service = get_object_or_404(Service, slug=service_slug, is_active=True)

    # 1. Permission checks
    if not request.user.is_client:
        messages.error(request, "Only clients can place orders.")
        return redirect(service.get_absolute_url())
    
    if request.user == service.seller:
        messages.error(request, "You cannot order your own service.")
        return redirect(service.get_absolute_url())

    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            # 2. Create the Order object
            order = form.save(commit=False)
            order.client = request.user
            order.seller = service.seller
            order.service = service
            order.price_at_order = service.price # Capture the price at the time of order
            order.save()
            
            # The save method generates the order_ref now that the PK is available
            order.order_ref = f"ORD-{timezone.now().strftime('%Y%m%d%H%M')}-{order.pk}"
            order.save()

            messages.success(request, f"Order for '{service.title}' placed successfully! Status: Pending.")
            return redirect('order_detail', pk=order.pk)
    
    # 3. Render confirmation page (or use a simple POST redirect on the detail page)
    # For now, we use a simple GET request context.
    context = {
        'service': service,
        'form': OrderCreationForm(),
    }
    return render(request, 'orders/create_order.html', context)


# --- Order Detail and Status Update ---

class OrderDetailView(OrderPermissionMixin, DetailView):
    """
    Displays order details. Accessible by both Client and Seller.
    """
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        
        # ... (Messaging Context) ...

        # Check if review button should be visible (Client + Completed Status + No existing review)
        review_exists = hasattr(order, 'review')

        if self.request.user == order.client and order.status == 'COMPLETED' and not review_exists:
            context['can_review'] = True 
        else:
            context['can_review'] = False
        
        # Pass existing review if it exists
        if review_exists:
            context['existing_review'] = order.review

        return context

# Function view to handle status updates via POST
@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Permission check: Must be the seller of the order
    if request.user != order.seller:
        return HttpResponseForbidden("You do not have permission to update this order status.")

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            
            # Set completion date if status is set to COMPLETED
            if order.status == 'COMPLETED' and not order.completion_date:
                order.completion_date = timezone.now()
                order.save()
                messages.success(request, f"Order {order.order_ref} marked as **Completed**.")
            
            elif order.status == 'CANCELLED':
                messages.warning(request, f"Order {order.order_ref} has been **Cancelled**.")
                
            else:
                messages.info(request, f"Order {order.order_ref} status updated to **{order.get_status_display()}**.")
                
            return redirect('order_detail', pk=order.pk)
    
    # If not POST or form invalid, redirect back to detail page
    messages.error(request, "Invalid status update attempt.")
    return redirect('order_detail', pk=order.pk)


# --- Order List Views for Dashboards ---

class ClientOrderListView(LoginRequiredMixin, ListView):
    """
    List of orders placed by the current Client (Dashboard view).
    """
    model = Order
    template_name = 'orders/order_list_client.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        # Filter orders only for the logged-in client
        if not self.request.user.is_client:
            return Order.objects.none()
        return Order.objects.filter(client=self.request.user).order_by('-created_at')

class SellerOrderListView(LoginRequiredMixin, ListView):
    """
    List of orders received by the current Seller (Dashboard view).
    """
    model = Order
    template_name = 'orders/order_list_seller.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        # Filter orders only for the logged-in seller
        if not self.request.user.is_seller:
            return Order.objects.none()
        return Order.objects.filter(seller=self.request.user).order_by('-created_at')