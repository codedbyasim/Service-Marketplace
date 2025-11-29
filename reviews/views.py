# reviews/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from orders.models import Order
from .models import Review
from .forms import ReviewForm

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        user = self.request.user

        # 1. Check if the user is the client for this order
        if user != self.order.client:
            messages.error(request, "You can only review orders you placed.")
            return redirect('order_detail', pk=self.order.pk)

        # 2. Check if the order is completed
        if self.order.status != 'COMPLETED':
            messages.error(request, "You can only review completed orders.")
            return redirect('order_detail', pk=self.order.pk)

        # 3. Check if a review already exists for this order
        if hasattr(self.order, 'review'):
            messages.warning(request, "This order has already been reviewed.")
            return redirect('order_detail', pk=self.order.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.client = self.request.user
        review.order = self.order
        review.service = self.order.service
        review.save()
        messages.success(self.request, f"Thank you for reviewing '{review.service.title}'! Your rating: {review.rating}/5")
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the service detail page or the order detail page
        return reverse('order_detail', kwargs={'pk': self.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['service'] = self.order.service
        return context