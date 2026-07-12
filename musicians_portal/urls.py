from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.dashboard, name='portal_dashboard'),
    path('portal/scores/', views.scores, name='portal_scores'),
    path('portal/scores/<int:song_id>/', views.song_detail, name='portal_song_detail'),

    # Calendar
    path('portal/calendar/', views.event_calendar, name='portal_calendar'),
    path('portal/calendar/partial/', views.calendar_month_partial, name='portal_calendar_partial'),
    path('portal/calendar/events/new/', views.event_create, name='portal_event_create'),
    path('portal/calendar/events/<int:event_id>/', views.event_detail, name='portal_event_detail'),
    path('portal/calendar/events/<int:event_id>/edit/', views.event_edit, name='portal_event_edit'),
    path('portal/calendar/events/<int:event_id>/delete/', views.event_delete, name='portal_event_delete'),
    path('portal/calendar/events/<int:event_id>/rsvp/', views.event_rsvp, name='portal_event_rsvp'),
    path('portal/calendar/sync/', views.sync_google_calendar, name='portal_calendar_sync'),

    # Gig logging
    path('portal/gigs/new/', views.gig_log, name='portal_gig_log'),

    # Musician pay
    path('portal/calendar/events/<int:event_id>/pay/', views.musician_pay_set, name='portal_musician_pay_set'),
    path('portal/calendar/events/<int:event_id>/pay/bulk/', views.musician_pay_bulk, name='portal_musician_pay_bulk'),
    path('portal/calendar/events/<int:event_id>/pay/mark-paid/', views.mark_event_paid, name='portal_mark_event_paid'),
    path('portal/calendar/events/<int:event_id>/guests/new/', views.guest_musician_create, name='portal_guest_create'),
    path('portal/calendar/events/<int:event_id>/guests/<int:musician_id>/deactivate/', views.guest_musician_deactivate, name='portal_guest_deactivate'),
    path('portal/pay/summary/', views.pay_summary, name='portal_pay_summary'),

    # Contracts (portal, finance-gated)
    path('portal/contracts/<int:contract_id>/', views.contract_detail, name='portal_contract_detail'),
    path('portal/calendar/events/<int:event_id>/contract/new/', views.contract_create, name='portal_contract_create'),
    path('portal/contracts/<int:contract_id>/send/email/', views.contract_send_email, name='portal_contract_send_email'),
    path('portal/contracts/<int:contract_id>/send/twilio/', views.contract_send_twilio, name='portal_contract_send_twilio'),
    path('portal/contracts/<int:contract_id>/mark-sent/', views.contract_mark_sent, name='portal_contract_mark_sent'),
    path('portal/contracts/<int:contract_id>/void/', views.contract_void, name='portal_contract_void'),

    # Contract signing (PUBLIC — the unguessable token is the capability)
    path('contract/<uuid:token>/', views.contract_sign, name='contract_sign'),
]
