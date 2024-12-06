from django.db import models

# Create your models here.
class Courses(models.Model):
    course_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank =True, null =True)
    course_image = models.TextField(blank=True, null=True)
    duration_in_weeks = models.PositiveIntegerField(help_text="Duration of the course in weeks")
    fee = models.DecimalField(max_digits=10, decimal_places=2, help_text="Course fee in local currency")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name
