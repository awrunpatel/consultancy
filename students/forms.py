from django import forms
from django.db import transaction
from userauth.models import AddressInfo, User, PersonalInfo
from students.models import Students
from courses.models import Courses
from userauth.forms import UserForm, AddressInfoForm, PersonalInfoForm

class StudentForm(forms.ModelForm):
    course_name = forms.ModelChoiceField(
        queryset=Courses.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control border-primary shadow-sm',
            'id': 'course_name',
            'data-placeholder': 'Select course',
        }),
        label='Course Name'
    )

    class Meta:
        model = Students
        fields = ['date_of_admission', 'shift','student_id','father_name', 'mother_name','course_name']
        widgets = {
            'date_of_admission': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'date_of_admission',
                'type': 'date',
                'placeholder': 'Date of Admission',
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
                'id': 'shift',
                'data-placeholder': 'Select shift',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_id',
                'placeholder': 'Student ID',
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'father_name',
                'placeholder': 'Father\'s Full Name',
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'mother_name',
                'placeholder': 'Mother\'s Full Name',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)


class StudentAddForm:
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        self.user_form = UserForm(data=data)
        self.permanent_address_form = AddressInfoForm(prefix="permanent", data=data)
        self.temporary_address_form = AddressInfoForm(prefix="temporary", data=data)
        self.personal_info_form = PersonalInfoForm(data=data)
        self.student_form = StudentForm(data=data, prefix="student")

    def is_valid(self):
        registration_forms = [
            self.user_form,
            self.permanent_address_form,
            self.temporary_address_form,
            self.personal_info_form,
            self.student_form
        ]
        return all(form.is_valid() for form in registration_forms)

    def save(self, commit=True):
        with transaction.atomic():
            user = self.user_form.save(commit=False)

            if commit:
                user.save()

            permanent_address = self.permanent_address_form.save(commit=False)
            temporary_address = self.temporary_address_form.save(commit=False)

            if commit:
                permanent_address.save()
                temporary_address.save()

            # Save Personal Info
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = permanent_address
            personal_info.temporary_address = temporary_address

            if commit:
                personal_info.save()

            # Save Student instance
            instance = self.student_form.save(commit=False)
            instance.user = user
            instance.personal_info = personal_info

            if commit:
                instance.save()

            return instance


class StudentEditForm:
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        personalinfo_instance = kwargs.pop('personalinfo_instance', None)
        data = kwargs.pop('data', None)

        if not instance:
            raise ValueError('Instance must be provided')

        if not personalinfo_instance:
            raise ValueError('Personal Info instance must be provided')

        self.user_form = UserForm(instance=instance.user, data=data)
        self.permanent_address_form = AddressInfoForm(prefix="permanent", data=data,
                                                      instance=personalinfo_instance.permanent_address)
        self.temporary_address_form = AddressInfoForm(prefix="temporary", data=data,
                                                      instance=personalinfo_instance.temporary_address)
        self.personal_info_form = PersonalInfoForm(instance=personalinfo_instance, data=data)
        self.student_form = StudentForm(prefix="student", instance=instance, data=data)

    def is_valid(self):
        registration_forms = [
            self.user_form,
            self.permanent_address_form,
            self.temporary_address_form,
            self.personal_info_form,
            self.student_form,
        ]
        return all(form.is_valid() for form in registration_forms)

    def save(self, commit=True):
        with transaction.atomic():
            user = self.user_form.save(commit=False)

            if commit:
                user.save()

            permanent_address = self.permanent_address_form.save(commit=False)
            temporary_address = self.temporary_address_form.save(commit=False)

            if commit:
                permanent_address.save()
                temporary_address.save()

            # Save Personal Info
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = permanent_address
            personal_info.temporary_address = temporary_address

            if commit:
                personal_info.save()

            # Save Student instance
            instance = self.student_form.save(commit=False)
            instance.user = user
            instance.personal_info = personal_info

            if commit:
                instance.save()

            return instance
