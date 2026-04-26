from django.db import models


class SiteMedia(models.Model):
    """
    Stores a single media file (image or video) for a named UI slot.
    Admins can upload or swap files from the Media Manager (/portal/media/).
    """
    SLOT_CHOICES = [
        # ── Images ──────────────────────────────────────────────────
        ('hero_image',    'Hero Photo (top of homepage)'),
        ('about_image',   'About Section Photo'),
        ('gallery_1',     'Gallery Photo 1'),
        ('gallery_2',     'Gallery Photo 2'),
        ('gallery_3',     'Gallery Photo 3'),
        ('gallery_4',     'Gallery Photo 4'),
        ('gallery_5',     'Gallery Photo 5'),
        ('gallery_6',     'Gallery Photo 6'),
        # ── Videos ──────────────────────────────────────────────────
        ('video_1',       'Video Showcase 1'),
        ('video_2',       'Video Showcase 2'),
        ('video_3',       'Video Showcase 3'),
        ('video_4',       'Video Showcase 4'),
    ]
    MEDIA_TYPE_IMAGE = 'image'
    MEDIA_TYPE_VIDEO = 'video'
    MEDIA_TYPE_CHOICES = [
        (MEDIA_TYPE_IMAGE, 'Image'),
        (MEDIA_TYPE_VIDEO, 'Video'),
    ]

    slot        = models.CharField(max_length=30, choices=SLOT_CHOICES, unique=True)
    media_type  = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default=MEDIA_TYPE_IMAGE)
    file        = models.FileField(upload_to='site_media/')
    alt_text    = models.CharField(max_length=200, blank=True)
    caption     = models.CharField(max_length=200, blank=True, help_text='Video title or gallery caption')
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slot']
        verbose_name = 'Site Media'
        verbose_name_plural = 'Site Media'

    def __str__(self):
        return f"{self.get_slot_display()} ({self.file.name.split('/')[-1]})"

    @property
    def is_image(self):
        return self.media_type == self.MEDIA_TYPE_IMAGE

    @property
    def is_video(self):
        return self.media_type == self.MEDIA_TYPE_VIDEO


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

