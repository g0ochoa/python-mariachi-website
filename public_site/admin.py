from django.contrib import admin
from .models import BookingRequest


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'event_type', 'submitted_at', 'is_read')
    list_filter = ('event_type', 'is_read', 'promo_opt_in')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_read',)
    ordering = ('-submitted_at',)

