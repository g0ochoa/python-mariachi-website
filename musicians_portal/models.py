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
    rate_per_hour   = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Rate charged per hour (admin/lead only)')
    total_charged   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Total amount charged to client (admin/lead only)')
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


class Gig(models.Model):
    EVENT_TYPE_CHOICES = [
        ('wedding',      'Wedding'),
        ('quinceanera',  'Quinceañera'),
        ('birthday',     'Birthday'),
        ('corporate',    'Corporate'),
        ('church',       'Church'),
        ('festival',     'Festival'),
        ('private',      'Private Party'),
        ('other',        'Other'),
    ]

    client_name     = models.CharField(max_length=200)
    event_type      = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    date            = models.DateField()
    start_time      = models.TimeField()
    end_time        = models.TimeField()
    venue           = models.CharField(max_length=200, blank=True)
    city            = models.CharField(max_length=100, blank=True)
    musicians_count = models.PositiveSmallIntegerField(default=1, help_text='Number of musicians at this gig')
    rate_per_hour   = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Rate charged per hour (total, not per musician)')
    total_charged   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Total amount charged to client')
    notes           = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']
        verbose_name = 'Gig'
        verbose_name_plural = 'Gigs'

    def __str__(self):
        return f"{self.date} — {self.client_name} ({self.get_event_type_display()})"

    @property
    def gig_number(self):
        """Human-readable reference: GIG-2026-001"""
        return f"GIG-{self.date.year}-{self.id:03d}"

    @property
    def hours_played(self):
        """Calculate hours played from start/end time."""
        from datetime import datetime, date
        start = datetime.combine(date.today(), self.start_time)
        end   = datetime.combine(date.today(), self.end_time)
        if end < start:          # past midnight
            from datetime import timedelta
            end += timedelta(days=1)
        delta = end - start
        return round(delta.total_seconds() / 3600, 2)


class MusicianPay(models.Model):
    """Tracks how much each musician is paid for a specific event."""
    event    = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='musician_pays',
    )
    musician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pay_records',
        limit_choices_to={'role__in': ['musician', 'lead', 'admin']},
    )
    amount     = models.DecimalField(max_digits=8, decimal_places=2, help_text='Amount paid to this musician for this event')
    notes      = models.CharField(max_length=200, blank=True, help_text='Optional note (e.g. cash, Venmo, etc.)')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pay_records_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'musician')
        ordering = ['event__date', 'musician__first_name']

    def __str__(self):
        return f"{self.musician} — {self.event} — ${self.amount}"
