from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.dashboard, name='portal_dashboard'),
    path('portal/scores/', views.scores, name='portal_scores'),
    path('portal/scores/<int:song_id>/', views.song_detail, name='portal_song_detail'),

    # Calendar
    path('portal/calendar/', views.event_calendar, name='portal_calendar'),
    path('portal/calendar/events/new/', views.event_create, name='portal_event_create'),
    path('portal/calendar/events/<int:event_id>/', views.event_detail, name='portal_event_detail'),
    path('portal/calendar/events/<int:event_id>/edit/', views.event_edit, name='portal_event_edit'),
    path('portal/calendar/events/<int:event_id>/delete/', views.event_delete, name='portal_event_delete'),
    path('portal/calendar/events/<int:event_id>/rsvp/', views.event_rsvp, name='portal_event_rsvp'),
    path('portal/calendar/sync/', views.sync_google_calendar, name='portal_calendar_sync'),
]
