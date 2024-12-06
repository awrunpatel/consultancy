from django import forms
from .models import *


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'website_name',
            'location',
            'contact_email',
            'contact_number',
            
            'website_fav',
            'website_logo',
            'website_baner',
        ]



class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            'user', 
            'subject', 
            'name', 
            'email', 
            'message', 
            'phone_number', 
            'country'
        ]
        widgets = {
            'subject': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone_number': 'Phone Number',
        }
        help_texts = {
            'email': 'Enter a valid email address.',
        }
