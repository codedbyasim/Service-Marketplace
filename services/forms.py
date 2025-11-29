# services/forms.py

from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('title', 'category', 'description', 'price', 'cover_image')
        # We exclude 'seller' and 'slug' as they are set programmatically in the view
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A catchy title for your service'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your service in detail'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in USD'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # Custom validation (optional)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price