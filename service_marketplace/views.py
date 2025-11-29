# service_marketplace/views.py

from django.shortcuts import render

# Note on parameter names: 
# The 404 handler MUST accept the 'exception' argument.
# The 500 handler MUST accept the 'request' argument.

def custom_404(request, exception):
    """
    Custom handler for 404 (Not Found) errors.
    """
    # The status code is automatically set to 404 by Django
    return render(request, '404.html', {}, status=404)

def custom_500(request):
    """
    Custom handler for 500 (Internal Server Error) errors.
    """
    return render(request, '500.html', {}, status=500)