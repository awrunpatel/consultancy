from django import forms
from userauth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user_password',
                'placeholder': 'Password'
            }
        ),
        label="Password",
        required=False  # Make password optional for editing existing users
    )

    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'first_name', 'middle_name', 'last_name', 'mobile_number', 'profile_image', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_username', 'placeholder': 'Username'}),
            'role': forms.Select(
                attrs={'class': 'form-control', 'id': 'user_role', 'data-placeholder': 'Select any of Option'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'id': 'user_email', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_first_name', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_middle_name', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_last_name', 'placeholder': 'Last Name'}),
            'mobile_number': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_mobile_number', 'placeholder': 'Mobile Number'}),
            'profile_image': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_profile_image', 'placeholder': 'Profile Image URL'}),
        }
