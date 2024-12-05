from django.db import models
from userauth.models import *
from django.contrib.humanize.templatetags import humanize
from .data import COUNTRY_CHOICES

# Create your models here.
class SiteSettings(models.Model):
    website_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_number = models.CharField(max_length=13)
    
    website_fav = models.TextField(blank=True, null=True)
    website_logo = models.TextField(blank=True, null=True)
    website_baner = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.website_name

    
class Enquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.TextField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        return humanize.naturaltime(self.date)
