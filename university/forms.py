from django import forms
from .models import University, UniversityCourse, Intake

# Form for University
class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'country', 'city', 'logo', 'website', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Name'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'logo': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce', 'placeholder': 'Description', 'rows': 3}),
        }

# Form for UniversityCourse
class UniversityCourseForm(forms.ModelForm):
    class Meta:
        model = UniversityCourse
        fields = ['name', 'university', 'level', 'duration_years', 'tuition_fee', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Name'}),
            'university': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in Years'}),
            'tuition_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tuition Fee'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce', 'placeholder': 'Course Description', 'rows': 3}),
        }

# Form for Intake
class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['course', 'intake_month', 'application_deadline']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'intake_month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Intake Month (e.g., September)'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
