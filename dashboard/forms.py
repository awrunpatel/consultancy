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
