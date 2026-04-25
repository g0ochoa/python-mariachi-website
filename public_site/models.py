from django.db import models


class BookingRequest(models.Model):
    """
    Stores contact/booking form submissions from the public site.
    Every time a visitor fills out the 'Contact Us' form,
    their information is saved here for Gerry to review in the admin panel.
    """
    EVENT_CHOICES = [
        ('wedding', 'Wedding'),
        ('quinceanera', 'Quinceañera'),
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('corporate', 'Corporate Event'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    message = models.TextField()
    promo_opt_in = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} - {self.get_event_type_display()} ({self.submitted_at.date()})"

