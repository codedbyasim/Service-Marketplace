# services/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q # For searching
from django.db.models import Avg
from .models import Service, Category
from .forms import ServiceForm
import uuid

# --- Helper Mixin for Sellers ---

class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to check if the user is logged in AND is a seller.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

# --- Client Facing Views (Browse/Search) ---

class ServiceListView(ListView):
    """
    Home page/Service listing with search, filtering, and pagination.
    """
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12 # Pagination

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        
        # 1. Search Logic (Q objects)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(seller__username__icontains=query)
            ).distinct()

        # 2. Filtering by Category
        category_slug = self.request.GET.get('category')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                queryset = queryset.filter(category=category)
                self.category = category
            except Category.DoesNotExist:
                pass # Ignore if category slug is invalid

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass all categories for the filter sidebar
        context['categories'] = Category.objects.all()
        context['current_category'] = getattr(self, 'category', None)
        context['query'] = self.request.GET.get('q', '')
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object

        # Fetch all related reviews, sorted by creation date
        context['reviews'] = service.reviews.all() 
        
        # The average_rating is calculated via the @property in the model, 
        # but we can explicitly pass it if needed, though it's available via service.average_rating
        # context['average_rating'] = service.average_rating 
        
        # Check if the current user is the seller of this service
        context['is_seller'] = self.request.user == service.seller
        
        return context

# --- Seller CRUD Views ---

class ServiceCreateView(SellerRequiredMixin, CreateView):
    """
    Seller can create a new service.
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('my_services')

    def form_valid(self, form):
        # Automatically set the seller and generate a slug
        service = form.save(commit=False)
        service.seller = self.request.user
        service.slug = uuid.uuid4().hex[:10] # Basic unique slug
        service.save()
        messages.success(self.request, f"Service '{service.title}' created successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

class ServiceUpdateView(SellerRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Seller can update their service. Only the creator can edit.
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        messages.success(self.request, f"Service '{self.object.title}' updated successfully!")
        return reverse_lazy('service_detail', kwargs={'slug': self.object.slug})

    def test_func(self):
        # Check if user is seller and is the service owner
        service = self.get_object()
        return service.seller == self.request.user and self.request.user.is_seller
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

class ServiceDeleteView(SellerRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Seller can delete their service. Only the creator can delete.
    """
    model = Service
    template_name = 'services/service_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('my_services')

    def test_func(self):
        # Check if user is seller and is the service owner
        service = self.get_object()
        return service.seller == self.request.user and self.request.user.is_seller

    def form_valid(self, form):
        messages.success(self.request, f"Service '{self.object.title}' deleted successfully!")
        return super().form_valid(form)

# My Services List
class MyServicesListView(SellerRequiredMixin, ListView):
    """
    List of services created by the currently logged-in seller.
    """
    model = Service
    template_name = 'services/my_services.html'
    context_object_name = 'services'
    paginate_by = 10

    def get_queryset(self):
        # Filter services only for the logged-in seller
        return Service.objects.filter(seller=self.request.user).order_by('-created_at')

# --- Admin Customization Helper (for initial setup) ---

def create_initial_categories(request):
    """
    A simple view to create a few initial categories for testing.
    Access this once via a temporary URL like /services/setup/
    """
    if not request.user.is_superuser:
        messages.error(request, "Only Superusers can run this setup.")
        return redirect('home')

    categories_to_add = [
        ('Web Development', 'web-development'),
        ('Graphic Design', 'graphic-design'),
        ('Digital Marketing', 'digital-marketing'),
        ('Writing & Translation', 'writing-translation'),
    ]
    
    count = 0
    for name, slug in categories_to_add:
        _, created = Category.objects.get_or_create(name=name, defaults={'slug': slug})
        if created:
            count += 1
            
    messages.success(request, f"Initial categories created: {count}")
    return redirect('home')