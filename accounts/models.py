from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model supporting both customers and musicians
class User(AbstractUser):
    """
    Custom user model with role-based access.
    Supports three user types:
    - customer: Public users who register for promos/bookings
    - musician: Band members with portal access
    - admin: Full system access (administrators)
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('musician', 'Musician'),
        ('lead',     'Lead'),
        ('admin',    'Administrator'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        default='customer',
        help_text='User role determines access permissions'
    )
    
    # Customer-specific fields
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Contact phone number'
    )
    promo_opt_in = models.BooleanField(
        default=False,
        help_text='Opted in to receive promotional emails'
    )
    
    # Musician-specific fields (nullable for customers)
    instrument = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='Primary instrument for musicians'
    )
    google_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        unique=True,
        help_text='Google Workspace ID for SSO authentication'
    )
    default_hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Default hourly pay rate for this musician (used in auto-calculate)',
    )
    is_test_account = models.BooleanField(
        default=False,
        help_text='Test/demo accounts are hidden from pay entry and pay summary',
    )
    active_from = models.DateField(
        null=True,
        blank=True,
        help_text='Date this musician joined the band (leave blank = always active from start)',
    )
    active_until = models.DateField(
        null=True,
        blank=True,
        help_text='Last date this musician was active (leave blank = still active)',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

