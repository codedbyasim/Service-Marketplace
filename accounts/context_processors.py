# accounts/context_processors.py

# You can add logic here if you want to pass common, user-specific data 
# to every template, but for now, we'll keep it simple to fix the error.

def user_profile_context(request):
    """
    Returns common context variables related to user roles.
    
    Placeholder function to satisfy the import error. 
    You might use this later to fetch things like unread chat counts 
    or dashboard links.
    """
    context = {}
    
    # Example: Check if the user is authenticated and set a flag
    if request.user.is_authenticated:
        context['is_client_user'] = request.user.is_client
        context['is_seller_user'] = request.user.is_seller
    else:
        context['is_client_user'] = False
        context['is_seller_user'] = False
        
    return context