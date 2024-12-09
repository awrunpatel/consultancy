from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('counselor', 'Counselor'),
]
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="student")
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Set is_staff based on role
        if self.role in ['admin']:
            self.is_superuser = True
        elif self.role in ['teacher','counseler']:
            self.is_staff = True
        else:
            self.is_staff = False

        # Generate a unique username if none is provided
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            unique_username = base_username
            counter = 1
            while User.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}_{counter}"
                counter += 1
            self.username = unique_username
        
        # Call the parent class's save() method to save the object
        super().save(*args, **kwargs)

    def get_full_name(self):
        full_name = self.full_name_raw()
        if full_name:
            return full_name
        else:
            return ""

    def full_name_raw(self):
        parts = [self.first_name or "", self.middle_name or "", self.last_name or ""]
        return " ".join(part for part in parts if part).strip()


class AddressInfo(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)


class EducationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    major_subject = models.CharField(max_length=100, null=True, blank=True)
    file = models.TextField(blank=True, null=True)

class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citizenship_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth_in_ad = models.DateField(null=True, blank=True)
    citizenship_img = models.TextField(null=True, blank=True)
    permanent_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='permanent_address',
                                          null=True, blank=True)
    temporary_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='temporary_address',
                                          null=True, blank=True)
