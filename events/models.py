from django.db import models

class Event(models.Model):
    EVENT_TYPES = [
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('counseling', 'Counseling Session'),
        ('fair', 'Education Fair'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the event")
    description = models.TextField(help_text="Detailed description of the event")
    event_image = models.TextField(blank=True, null=True, help_text="Image or banner for the event")
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, help_text="Type of event")
    start_date = models.DateField(help_text="Start date of the event")
    end_date = models.DateField(blank=True, null=True, help_text="End date of the event (if applicable)")
    start_time = models.TimeField(blank=True, null=True, help_text="Start time of the event")
    end_time = models.TimeField(blank=True, null=True, help_text="End time of the event")
    location = models.CharField(max_length=255, help_text="Location or platform (for online events)")
    is_online = models.BooleanField(default=False, help_text="Is this event held online?")
    registration_required = models.BooleanField(default=True, help_text="Is registration required?")
    registration_link = models.URLField(blank=True, null=True, help_text="Registration link for online registration")
    contact_email = models.EmailField(help_text="Contact email for queries")
    max_participants = models.PositiveIntegerField(blank=True, null=True, help_text="Maximum number of participants")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the event was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time when the event was last updated")
    is_active = models.BooleanField(default=True, help_text="Is this event active?")

    def __str__(self):
        return self.title

    def is_past_event(self):
        """
        Check if the event has already occurred.
        """
        from datetime import date
        return self.end_date and self.end_date < date.today()

    def get_duration(self):
        """
        Calculate the duration of the event in days.
        """
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1  # Single-day event by default
