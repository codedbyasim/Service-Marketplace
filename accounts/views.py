# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse_lazy
from orders.models import Order
from .forms import ClientRegistrationForm, SellerRegistrationForm, UserProfileForm
from .models import User, UserProfile

# --- Authentication Views ---

# 1. Custom Login View (using built-in)
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    # success_url is handled by LOGIN_REDIRECT_URL in settings.py

# 2. Logout View (using built-in)
class CustomLogoutView(LogoutView):
    # next_page is handled by LOGOUT_REDIRECT_URL in settings.py
    pass

# 3. Client Registration View
class ClientRegisterView(CreateView):
    model = User
    form_class = ClientRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'client'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Client account created successfully! Please log in.")
        return response

# 4. Seller Registration View
class SellerRegisterView(CreateView):
    model = User
    form_class = SellerRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'seller'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Seller account created successfully! Please log in.")
        return response

# --- Dashboard & Profile Views ---

@login_required
def dashboard_view(request):
    """
    Directs the user to the appropriate dashboard based on their role.
    """
    user = request.user
    if user.is_seller:
        return redirect('seller_dashboard')
    elif user.is_client:
        return redirect('client_dashboard')
    
    messages.warning(request, "Your account role is not defined.")
    return redirect('home')

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        messages.error(request, "Access denied. You are not a seller.")
        return redirect('dashboard')
    
    # Fetch seller specific stats
    total_orders = Order.objects.filter(seller=request.user).count()
    completed_orders = Order.objects.filter(seller=request.user, status='COMPLETED')
    total_earnings = sum(order.price_at_order for order in completed_orders)
    
    context = {
        'user': request.user, 
        'dashboard_type': 'Seller',
        'total_orders': total_orders,
        'total_earnings': total_earnings,
        'latest_orders': Order.objects.filter(seller=request.user).order_by('-created_at')[:5],
    }
    return render(request, 'accounts/seller_dashboard.html', context)

@login_required
def client_dashboard(request):
    if not request.user.is_client:
        messages.error(request, "Access denied. You are not a client.")
        return redirect('dashboard')
        
    # Fetch client specific stats
    completed_orders = Order.objects.filter(client=request.user, status='COMPLETED')
    total_spent = sum(order.price_at_order for order in completed_orders)

    context = {
        'user': request.user, 
        'dashboard_type': 'Client',
        'total_spent': total_spent,
        'latest_orders': Order.objects.filter(client=request.user).order_by('-created_at')[:5],
    }
    return render(request, 'accounts/client_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_update.html'
    # Use reverse_lazy for the success URL
    success_url = reverse_lazy('dashboard') 

    def get_object(self, queryset=None):
        # Ensure only the current user's profile is edited
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)