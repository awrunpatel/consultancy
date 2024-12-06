from django import forms
from .models import Courses

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = [
            'course_name', 
            'description',
            'course_image',
            'duration_in_weeks', 
            'fee', 
            'start_date', 
            'end_date', 
            'is_active'
        ]
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce', 'placeholder': 'Course Description'}),
            'course_image': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'course_image', 'placeholder': 'Course Image'}),
            'duration_in_weeks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in weeks'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Course Fee'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'course_name': 'Course Name',
            'description': 'Description',
            'course_image':'Course image',
            'duration_in_weeks': 'Duration (in weeks)',
            'fee': 'Fee (in local currency)',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'is_active': 'Is Active?',
        }
