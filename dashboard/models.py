from django.db import models

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

    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'

