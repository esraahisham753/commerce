from django import forms

from .models import User, Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_bid', 'image', 'category']
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(attrs={'class': 'form-control'}),
        'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
        'image': forms.URLInput(attrs={'class': 'form-control'}),
        'category': forms.TextInput(attrs={'class': 'form-control'}),
    }

