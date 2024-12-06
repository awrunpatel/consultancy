from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 
            'description', 
            'event_image',
            'event_type', 
            'start_date', 
            'end_date', 
            'start_time', 
            'end_time', 
            'location', 
            'is_online', 
            'registration_required', 
            'registration_link', 
            'contact_email', 
            'max_participants', 
            'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce'}),
            'event_image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter event image URL'}),  # URLInput instead of TextInput for image upload
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location or platform'}),
            'is_online': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'registration_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'registration_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter registration link'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact email'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter maximum participants'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            'title': 'Event Title',
            'description': 'Description',
            'event_image': 'Event Image',
            'event_type': 'Event Type',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'location': 'Location',
            'is_online': 'Is Online?',
            'registration_required': 'Requires Registration?',
            'registration_link': 'Registration Link',
            'contact_email': 'Contact Email',
            'max_participants': 'Maximum Participants',
            'is_active': 'Is Active?',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date and end_date < start_date:
            self.add_error('end_date', "End date cannot be earlier than the start date.")
        
        return cleaned_data
