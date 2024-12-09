from django.db import models
from dashboard.data import COUNTRY_CHOICES

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=100)
    logo = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

class UniversityCourse(models.Model):
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
    ]

    name = models.CharField(max_length=200)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="courses")
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    duration_years = models.IntegerField()
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.level}) - {self.university.name}"

class Intake(models.Model):
    course = models.ForeignKey(UniversityCourse, on_delete=models.CASCADE, related_name="intakes")
    intake_month = models.CharField(max_length=50)
    application_deadline = models.DateField()

    def __str__(self):
        return f"{self.course.name} - {self.intake_month}"
