from django import forms

from students.models import Students
from userauth.models import (
    User, PersonalInfo, AddressInfo, EducationHistory
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if user.role == "student":
            Students.objects.get_or_create(user=user)
        
        if commit:
            user.save()
        return user
       

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'profile_image','mobile_number']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'id': 'user_email', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_first_name', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_middle_name', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_last_name', 'placeholder': 'Last Name'}),
            'profile_image': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_profile_image', 'placeholder': 'Profile Image'}),
        }


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['citizenship_number', 'gender', 'date_of_birth_in_ad', 'citizenship_img']
        widgets = {
            'citizenship_number': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'citizenship_number', 'placeholder': 'Citizenship Number'}),
            'gender': forms.Select(
                attrs={'class': 'form-control', 'id': 'gender', 'data-placeholder': 'Select any of Option'}),
            'date_of_birth_in_ad': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'date_of_birth_in_ad', 'type': 'date',
                       'placeholder': 'Date of Birth'}),
            'citizenship_img': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'citizenship_img', 'placeholder': 'Citizenship Image URL'}),
        }


class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city', 'placeholder': 'City'}),
            'province': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'province', 'placeholder': 'Province/State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country', 'placeholder': 'Country'}),
            'postcode': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'postcode', 'placeholder': 'Postal Code'}),
            'contact_number': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'contact_number', 'placeholder': 'Contact Number'}),
        }


class EducationHistoryForm(forms.ModelForm):
    class Meta:
        model = EducationHistory
        fields = ['degree_name', 'institution_name', 'graduation_year', 'major_subject', 'file']
        widgets = {
            'degree_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'degree_name', 'placeholder': 'Degree Name'}),
            'institution_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'institution_name', 'placeholder': 'Institution Name'}),
            'graduation_year': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'graduation_year', 'placeholder': 'Graduation Year'}),
            'major_subject': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'major_subject', 'placeholder': 'Major Subject'}),
            'file': forms.TextInput(attrs={'class': 'form-control', 'id': 'file', 'placeholder': 'File URL'}),
        }
