import uuid

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
        ('absence',   'Absence'),
        ('other',     'Other'),
    ]

    title      = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='gig')
    date       = models.DateField()
    end_date   = models.DateField(null=True, blank=True, help_text='Last day of multi-day events (leave blank for single-day)')
    start_time = models.TimeField(null=True, blank=True)
    end_time   = models.TimeField(null=True, blank=True)
    venue      = models.CharField(max_length=200, blank=True)
    client     = models.CharField(max_length=200, blank=True)
    notes           = models.TextField(blank=True)
    google_event_id = models.CharField(max_length=300, blank=True, db_index=True)
    rate_per_hour   = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Rate charged per hour (admin/lead only)')
    total_charged   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Total amount charged to client (admin/lead only)')
    billed_hours    = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Actual hours billed (overrides start/end time calculation)')
    is_paid     = models.BooleanField(default=False, help_text='Marked by admin/lead once the client has paid the band')
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
    client_phone    = models.CharField(max_length=30, blank=True)
    client_email    = models.EmailField(blank=True)
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


class ContractTemplate(models.Model):
    """Editable master contract terms (django-admin). New contracts snapshot
    these at creation, so editing the template never changes sent contracts."""
    name       = models.CharField(max_length=100, default='Standard Gig Contract')
    terms_en   = models.TextField(help_text='English contract terms')
    terms_es   = models.TextField(help_text='Spanish contract terms')
    is_active  = models.BooleanField(default=True, help_text='The active template used for new contracts')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Contract(models.Model):
    """A gig contract sent to a client for electronic acknowledgment.
    Everything the client sees is snapshotted at creation (client info, event
    facts, financials, terms) — later Event/template edits don't mutate it.
    Changes after sending = void this contract and create a fresh one."""
    STATUS_CHOICES = [
        ('draft',  'Draft'),
        ('sent',   'Sent'),
        ('signed', 'Signed'),
        ('voided', 'Voided'),
    ]
    LANGUAGE_CHOICES = [('en', 'English'), ('es', 'Español')]
    SENT_VIA_CHOICES = [
        ('sms',    'SMS composer'),
        ('email',  'Email'),
        ('twilio', 'Twilio SMS'),
        ('link',   'Link copied'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='contracts')
    gig   = models.ForeignKey(Gig, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Client (snapshot)
    client_name  = models.CharField(max_length=200)
    client_phone = models.CharField(max_length=30, blank=True)
    client_email = models.EmailField(blank=True)

    # Event facts (snapshot)
    event_type_label = models.CharField(max_length=50, blank=True)
    event_date       = models.DateField()
    start_time       = models.TimeField(null=True, blank=True)
    end_time         = models.TimeField(null=True, blank=True)
    venue            = models.CharField(max_length=200, blank=True)
    city             = models.CharField(max_length=100, blank=True)

    # Financials (snapshot)
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    overtime_rate  = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                                         help_text='Overtime rate per hour')

    # Terms snapshot
    terms_en = models.TextField()
    terms_es = models.TextField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='es',
                                help_text='Default language shown to the client')

    # Lifecycle
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    sent_via  = models.CharField(max_length=10, choices=SENT_VIA_CHOICES, blank=True)
    sent_at   = models.DateTimeField(null=True, blank=True)
    voided_at = models.DateTimeField(null=True, blank=True)

    # Signature audit (clickwrap)
    signed_name       = models.CharField(max_length=200, blank=True)
    signed_at         = models.DateTimeField(null=True, blank=True)
    signed_ip         = models.GenericIPAddressField(null=True, blank=True)
    signed_user_agent = models.CharField(max_length=500, blank=True)
    signed_language   = models.CharField(max_length=2, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name='contracts_created')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contract_number} — {self.client_name} ({self.status})"

    @property
    def contract_number(self):
        return f"CT-{self.event_date.year}-{self.id:03d}"

    @property
    def balance_due(self):
        if self.total_amount is not None and self.deposit_amount is not None:
            return self.total_amount - self.deposit_amount
        return None


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
    is_paid    = models.BooleanField(default=False, help_text='Set by admin/lead once this musician has been paid')
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
