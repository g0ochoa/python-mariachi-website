from django.contrib import admin
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display  = ('title', 'genre', 'difficulty', 'has_audio', 'has_score', 'file_count', 'is_active')
    list_filter   = ('genre', 'difficulty', 'has_audio', 'has_score', 'is_active')
    search_fields = ('title', 'folder_name')
    list_editable = ('genre', 'difficulty', 'is_active')
