from django.contrib import admin
from django.db.models import Sum, Count, Avg
from django.urls import reverse
from django.utils.html import format_html
from .models import Song, Gig, MusicianPay, Contract, ContractTemplate


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display  = ('title', 'genre', 'difficulty', 'has_audio', 'has_score', 'file_count', 'is_active')
    list_filter   = ('genre', 'difficulty', 'has_audio', 'has_score', 'is_active')
    search_fields = ('title', 'folder_name')
    list_editable = ('genre', 'difficulty', 'is_active')


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display  = (
        'gig_number', 'date', 'client_name', 'event_type_badge', 'city',
        'start_time', 'end_time', 'hours_played_display',
        'musicians_count', 'rate_per_hour', 'total_charged',
    )
    list_filter   = ('event_type', 'date', 'city')
    search_fields = ('client_name', 'venue', 'city', 'notes')
    date_hierarchy = 'date'
    ordering      = ('-date', '-start_time')
    readonly_fields = ('hours_played_display', 'created_at')

    fieldsets = (
        ('Event Details', {
            'fields': ('client_name', 'event_type', 'date', 'start_time', 'end_time', 'hours_played_display'),
        }),
        ('Location', {
            'fields': ('venue', 'city'),
        }),
        ('Financials', {
            'fields': ('musicians_count', 'rate_per_hour', 'total_charged'),
            'description': 'Financial data — fill in when available.',
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def event_type_badge(self, obj):
        colors = {
            'wedding':     '#e91e8c',
            'quinceanera': '#9c27b0',
            'birthday':    '#ff9800',
            'corporate':   '#2196f3',
            'church':      '#4caf50',
            'festival':    '#f44336',
            'private':     '#607d8b',
            'other':       '#9e9e9e',
        }
        color = colors.get(obj.event_type, '#9e9e9e')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px">{}</span>',
            color, obj.get_event_type_display()
        )
    event_type_badge.short_description = 'Type'

    def hours_played_display(self, obj):
        return f"{obj.hours_played} hrs"
    hours_played_display.short_description = 'Hours'

    def changelist_view(self, request, extra_context=None):
        """Add summary stats to the list view."""
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        stats = qs.aggregate(
            total_gigs=Count('id'),
            total_revenue=Sum('total_charged'),
            avg_musicians=Avg('musicians_count'),
        )
        response.context_data['summary'] = stats
        return response


@admin.register(ContractTemplate)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'updated_at')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display    = ('contract_number', 'client_name', 'event_date', 'status', 'language',
                       'sent_via', 'sent_at', 'signed_at')
    list_filter     = ('status', 'language', 'event_date')
    search_fields   = ('client_name', 'client_phone', 'client_email', 'venue')
    readonly_fields = ('token', 'public_link', 'signed_name', 'signed_at', 'signed_ip',
                       'signed_user_agent', 'signed_language', 'created_at')
    raw_id_fields   = ('event', 'gig')
    date_hierarchy  = 'event_date'

    def public_link(self, obj):
        url = reverse('contract_sign', args=[obj.token])
        return format_html('<a href="{}" target="_blank" rel="noopener">{}</a>', url, url)
    public_link.short_description = 'Signing link'


@admin.register(MusicianPay)
class MusicianPayAdmin(admin.ModelAdmin):
    list_display  = ('musician', 'event', 'amount', 'notes', 'created_by', 'created_at')
    list_filter   = ('event__date', 'musician')
    search_fields = ('musician__first_name', 'musician__last_name', 'musician__username', 'event__title', 'notes')
    raw_id_fields = ('event',)
    readonly_fields = ('created_at', 'created_by')
    date_hierarchy = 'event__date'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
