import uuid

from django.db import models, transaction
from django.utils import timezone

from userauth.models import AddressInfo, User, PersonalInfo
from courses.models import Courses


class Students(models.Model):
    SHIFT = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
    ]

    # Details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True, default=timezone.now)
    shift = models.CharField(max_length=50, choices=SHIFT, null=True, blank=True)
    father_name = models.TextField(max_length=100, blank=True, null=True)
    mother_name = models.TextField(max_length=100, blank=True, null=True)
    course_name = models.ForeignKey(Courses, on_delete=models.CASCADE)
