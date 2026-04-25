from django.db import models


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
