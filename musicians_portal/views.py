import os
import calendar
import threading
from datetime import date, datetime, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests as http_requests
from icalendar import Calendar as iCalendar

BAND_TZ = ZoneInfo('America/Chicago')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Song, Event, EventAttendance

GCAL_SYNC_CACHE_KEY    = 'gcal_last_sync'
GCAL_SYNC_INTERVAL     = 30 * 60   # seconds — re-sync at most every 30 minutes

GOOGLE_ICAL_URL = os.environ.get('GOOGLE_ICAL_URL', '')


def _detect_event_type(summary):
    lower = summary.lower()
    if any(w in lower for w in ['ensayo', 'rehearsal', 'practice', 'practica']):
        return 'rehearsal'
    return 'gig'


def _do_ical_sync():
    """Fetch Google Calendar iCal feed and sync events into the DB.
    Returns (created, updated, deleted) counts, or None if URL not configured."""
    if not GOOGLE_ICAL_URL:
        return None
    try:
        resp = http_requests.get(GOOGLE_ICAL_URL, timeout=15)
        resp.raise_for_status()
        gcal = iCalendar.from_ical(resp.content)
    except Exception:
        return None

    created = updated = deleted = 0
    seen_uids = set()

    for component in gcal.walk():
        if component.name != 'VEVENT':
            continue

        uid     = str(component.get('UID', ''))
        summary = str(component.get('SUMMARY', 'Untitled') or 'Untitled').strip()
        dtstart = component.get('DTSTART')
        dtend   = component.get('DTEND') or component.get('DTSTART')

        if dtstart is None:
            continue

        dtstart_val = dtstart.dt
        dtend_val   = dtend.dt

        if isinstance(dtstart_val, datetime):
            # Convert timezone-aware datetimes to CDT before extracting date/time
            if dtstart_val.tzinfo is not None:
                dtstart_val = dtstart_val.astimezone(BAND_TZ)
            event_date = dtstart_val.date()
            start_time = dtstart_val.time()
        else:
            event_date = dtstart_val
            start_time = None

        if isinstance(dtend_val, datetime):
            if dtend_val.tzinfo is not None:
                dtend_val = dtend_val.astimezone(BAND_TZ)
            end_time = dtend_val.time()
        else:
            end_time = None

        location    = str(component.get('LOCATION',    '') or '').strip()
        description = str(component.get('DESCRIPTION', '') or '').strip()

        seen_uids.add(uid)

        defaults = {
            'title':      summary[:200],
            'event_type': _detect_event_type(summary),
            'date':       event_date,
            'start_time': start_time,
            'end_time':   end_time,
            'venue':      location[:200],
            'notes':      description[:2000],
        }

        obj, was_created = Event.objects.update_or_create(
            google_event_id=uid,
            defaults=defaults,
        )
        if was_created:
            created += 1
        else:
            updated += 1

    stale_qs = Event.objects.exclude(google_event_id='').exclude(google_event_id__in=seen_uids)
    deleted  = stale_qs.count()
    stale_qs.delete()

    cache.set(GCAL_SYNC_CACHE_KEY, True, GCAL_SYNC_INTERVAL)
    return created, updated, deleted

SCORES_BASE_PATH = '/var/www/mariachiesencia/scores/'


def _make_file_dict(display_name, relative_path, folder_name):
    AUDIO_EXTS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac'}
    IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.tif', '.tiff'}
    ext = os.path.splitext(display_name)[1].lower()

    # URL-encode each path segment, preserving slashes
    folder_encoded   = quote(folder_name)
    relative_encoded = '/'.join(quote(part) for part in relative_path.split('/'))
    url = f'https://mariachiesencia.com/scores/{folder_encoded}/{relative_encoded}'

    if ext == '.pdf':
        kind, icon, color = 'pdf',   'bi-file-earmark-music-fill', 'text-danger'
    elif ext in AUDIO_EXTS:
        kind, icon, color = 'audio', 'bi-volume-up-fill',           'text-success'
    elif ext in IMAGE_EXTS:
        kind, icon, color = 'image', 'bi-file-earmark-image-fill',  'text-info'
    else:
        kind, icon, color = 'other', 'bi-file-earmark-fill',        'text-muted'

    return {
        'name':  display_name,
        'url':   url,
        'kind':  kind,
        'icon':  icon,
        'color': color,
        'ext':   ext.lstrip('.').upper() if ext else '?',
    }


def _scan_song_folder(folder_name):
    folder_path = os.path.join(SCORES_BASE_PATH, folder_name)
    if not os.path.exists(folder_path):
        return []
    result = []
    try:
        entries = sorted(os.scandir(folder_path), key=lambda e: (e.is_dir(), e.name.lower()))
    except PermissionError:
        return []
    for entry in entries:
        if entry.is_file():
            result.append(_make_file_dict(entry.name, entry.name, folder_name))
        elif entry.is_dir():
            try:
                for sub in sorted(os.scandir(entry.path), key=lambda e: e.name.lower()):
                    if sub.is_file():
                        result.append(_make_file_dict(sub.name, f'{entry.name}/{sub.name}', folder_name))
            except PermissionError:
                pass
    return result


@login_required
def dashboard(request):
    """
    Musicians portal dashboard.
    - @login_required: Django redirects unauthenticated users to LOGIN_URL
      (set to 'login' in settings).
    - Role check: Only musicians and admins can enter. Customers get a 403.
    """
    if request.user.role not in ('musician', 'admin'):
        raise PermissionDenied

    context = {
        'page_title': 'Musicians Portal',
    }
    return render(request, 'musicians_portal/dashboard.html', context)


@login_required
def scores(request):
    if request.user.role not in ('musician', 'admin'):
        raise PermissionDenied

    songs = Song.objects.filter(is_active=True).order_by('title')

    available_letters = sorted(set(
        s.title[0].upper() for s in songs if s.title
    ))

    context = {
        'page_title': 'Scores Library',
        'songs':      songs,
        'total':      songs.count(),
        'query':      '',
        'available_letters': available_letters,
    }
    return render(request, 'musicians_portal/scores.html', context)


@login_required
def song_detail(request, song_id):
    if request.user.role not in ('musician', 'admin'):
        raise PermissionDenied

    song  = get_object_or_404(Song, id=song_id, is_active=True)
    files = _scan_song_folder(song.folder_name)

    prev_song = Song.objects.filter(is_active=True, title__lt=song.title).order_by('-title').first()
    next_song = Song.objects.filter(is_active=True, title__gt=song.title).order_by('title').first()

    context = {
        'page_title': song.title,
        'song':       song,
        'files':      files,
        'prev_song':  prev_song,
        'next_song':  next_song,
    }
    return render(request, 'musicians_portal/song_detail.html', context)


# ─── Calendar ────────────────────────────────────────────────────────────────

def _require_portal(request):
    """Raise PermissionDenied if user is not musician or admin."""
    if request.user.role not in ('musician', 'admin'):
        raise PermissionDenied


@login_required
def calendar_month_partial(request):
    """Returns just the calendar grid HTML fragment for AJAX month navigation."""
    _require_portal(request)
    today = date.today()
    year  = int(request.GET.get('year',  today.year))
    month = int(request.GET.get('month', today.month))
    if month < 1:  month = 12; year -= 1
    if month > 12: month = 1;  year += 1

    cal        = calendar.monthcalendar(year, month)
    month_name = date(year, month, 1).strftime('%B %Y')

    events_this_month = Event.objects.filter(date__year=year, date__month=month)
    events_by_day = {}
    for ev in events_this_month:
        events_by_day.setdefault(ev.date.day, []).append(ev)

    prev_month = (date(year, month, 1) - timedelta(days=1)).replace(day=1)
    next_month = (date(year, month, 1) + timedelta(days=32)).replace(day=1)

    context = {
        'year': year, 'month': month, 'month_name': month_name,
        'cal': cal, 'events_by_day': events_by_day, 'today': today,
        'prev_year': prev_month.year, 'prev_month': prev_month.month,
        'next_year': next_month.year, 'next_month': next_month.month,
    }
    return render(request, 'musicians_portal/partials/calendar_month.html', context)


@login_required
def event_calendar(request):
    _require_portal(request)

    today = date.today()
    year  = int(request.GET.get('year',  today.year))
    month = int(request.GET.get('month', today.month))

    # Clamp to valid month range
    if month < 1:  month = 12; year -= 1
    if month > 12: month = 1;  year += 1

    # Build calendar grid (6 rows × 7 cols, None for padding)
    cal        = calendar.monthcalendar(year, month)
    month_name = date(year, month, 1).strftime('%B %Y')

    # Auto-sync Google Calendar if the cache has expired (non-blocking)
    if not cache.get(GCAL_SYNC_CACHE_KEY):
        threading.Thread(target=_do_ical_sync, daemon=True).start()

    # All events this month
    events_this_month = Event.objects.filter(date__year=year, date__month=month)
    events_by_day = {}
    for ev in events_this_month:
        events_by_day.setdefault(ev.date.day, []).append(ev)

    # Upcoming events (next 60 days) for list below grid
    upcoming = list(Event.objects.filter(
        date__gte=today, date__lte=today + timedelta(days=60)
    ).order_by('date', 'start_time'))

    # Build a dict of {event_id: rsvp_status} for the current user
    user_rsvp = {
        a.event_id: a.status
        for a in EventAttendance.objects.filter(
            event__in=upcoming, user=request.user
        )
    }

    # Previous / next month links
    prev_month = date(year, month, 1) - timedelta(days=1)
    next_month = date(year, month, 1) + timedelta(days=32)
    prev_month = prev_month.replace(day=1)
    next_month = next_month.replace(day=1)

    context = {
        'page_title':    'Event Calendar',
        'year':          year,
        'month':         month,
        'month_name':    month_name,
        'cal':           cal,
        'events_by_day': events_by_day,
        'today':         today,
        'upcoming':      upcoming,
        'next_up':       upcoming[:3],
        'user_rsvp':     user_rsvp,
        'prev_year':     prev_month.year,
        'prev_month':    prev_month.month,
        'next_year':     next_month.year,
        'next_month':    next_month.month,
    }
    return render(request, 'musicians_portal/calendar.html', context)


@login_required
def event_detail(request, event_id):
    _require_portal(request)

    event = get_object_or_404(Event, id=event_id)

    # Get or create an attendance record for current user
    attendance, _ = EventAttendance.objects.get_or_create(
        event=event, user=request.user,
        defaults={'status': 'pending'},
    )

    # All attendance records for display
    all_attendance = EventAttendance.objects.filter(event=event).select_related('user').order_by('user__first_name')

    context = {
        'page_title':    event.title,
        'event':         event,
        'attendance':    attendance,
        'all_attendance': all_attendance,
    }
    return render(request, 'musicians_portal/event_detail.html', context)


@login_required
@require_POST
def event_rsvp(request, event_id):
    """Musician marks themselves confirmed or unavailable."""
    _require_portal(request)

    event  = get_object_or_404(Event, id=event_id)
    status = request.POST.get('status')
    if status not in ('confirmed', 'unavailable', 'pending'):
        return JsonResponse({'error': 'invalid status'}, status=400)

    attendance, _ = EventAttendance.objects.get_or_create(event=event, user=request.user)
    attendance.status = status
    attendance.save()

    return redirect('portal_event_detail', event_id=event_id)


@login_required
def event_create(request):
    _require_portal(request)
    if request.user.role != 'admin':
        raise PermissionDenied

    if request.method == 'POST':
        p = request.POST
        event = Event.objects.create(
            title      = p['title'],
            event_type = p.get('event_type', 'gig'),
            date       = p['date'],
            start_time = p.get('start_time') or None,
            end_time   = p.get('end_time')   or None,
            venue      = p.get('venue', ''),
            client     = p.get('client', ''),
            notes      = p.get('notes', ''),
            created_by = request.user,
        )
        return redirect('portal_event_detail', event_id=event.id)

    context = {'page_title': 'Add Event'}
    return render(request, 'musicians_portal/event_form.html', context)


@login_required
def event_edit(request, event_id):
    _require_portal(request)
    if request.user.role != 'admin':
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        p = request.POST
        event.title      = p['title']
        event.event_type = p.get('event_type', 'gig')
        event.date       = p['date']
        event.start_time = p.get('start_time') or None
        event.end_time   = p.get('end_time')   or None
        event.venue      = p.get('venue', '')
        event.client     = p.get('client', '')
        event.notes      = p.get('notes', '')
        event.save()
        return redirect('portal_event_detail', event_id=event.id)

    context = {'page_title': 'Edit Event', 'event': event}
    return render(request, 'musicians_portal/event_form.html', context)


@login_required
@require_POST
def event_delete(request, event_id):
    _require_portal(request)
    if request.user.role != 'admin':
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)
    year, month = event.date.year, event.date.month
    event.delete()
    return redirect(f'/portal/calendar/?year={year}&month={month}')


@login_required
@require_POST
def sync_google_calendar(request):
    """Force a manual sync (admin only), bypassing the cache cooldown."""
    _require_portal(request)
    if request.user.role != 'admin':
        raise PermissionDenied

    cache.delete(GCAL_SYNC_CACHE_KEY)
    result = _do_ical_sync()
    if result is None:
        return JsonResponse({'error': 'GOOGLE_ICAL_URL not configured'}, status=502)
    created, updated, deleted = result
    return JsonResponse({'created': created, 'updated': updated, 'deleted': deleted})
