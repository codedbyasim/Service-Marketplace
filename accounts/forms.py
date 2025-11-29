# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile

# 1. Registration Form
class ClientRegistrationForm(UserCreationForm):
    """
    Client registration form. Inherits standard fields.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username') # Removed 'password' as it's handled by parent

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_client = True
        user.is_seller = False # Explicitly set roles
        if commit:
            user.save()
        return user

class SellerRegistrationForm(UserCreationForm):
    """
    Seller registration form.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_seller = True
        user.is_client = False
        if commit:
            user.save()
        return user

# 2. Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'bio', 'profile_image')