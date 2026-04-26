from django.db import models
from django.conf import settings


class Song(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy',   'Easy'),
        ('medium', 'Medium'),
        ('hard',   'Hard'),
    ]

    GENRE_CHOICES = [
        ('ranchera',   'Ranchera'),
        ('bolero',     'Bolero'),
        ('son',        'Son'),
        ('cumbia',     'Cumbia'),
        ('norteña',    'Norteña'),
        ('huapango',   'Huapango'),
        ('vals',       'Vals'),
        ('corrido',    'Corrido'),
        ('pop',        'Pop'),
        ('other',      'Other'),
    ]

    title       = models.CharField(max_length=200)
    folder_name = models.CharField(max_length=200, unique=True)
    genre       = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    difficulty  = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    has_audio   = models.BooleanField(default=False)
    has_score   = models.BooleanField(default=True)
    file_count  = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    added_at    = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Event(models.Model):
    TYPE_CHOICES = [
        ('gig',       'Gig'),
        ('rehearsal', 'Rehearsal'),
        ('other',     'Other'),
    ]

    title      = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='gig')
    date       = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time   = models.TimeField(null=True, blank=True)
    venue      = models.CharField(max_length=200, blank=True)
    client     = models.CharField(max_length=200, blank=True)
    notes           = models.TextField(blank=True)
    google_event_id = models.CharField(max_length=300, blank=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.date} — {self.title}"


class EventAttendance(models.Model):
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('confirmed',   'Confirmed'),
        ('unavailable', 'Unavailable'),
    ]

    event  = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    user   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_attendances',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note   = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user} / {self.event} — {self.status}"
