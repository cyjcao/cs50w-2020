from django import forms
from django.forms import ModelForm

from .models import Listing

class ListingForm(ModelForm):
    starting_bid = forms.DecimalField(label='Starting Bid', max_digits=10, decimal_places=2)

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'category'] + ['starting_bid']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control-file'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }