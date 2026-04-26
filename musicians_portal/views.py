import os
import calendar
from datetime import date, timedelta
from urllib.parse import quote

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Song, Event, EventAttendance

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

    # All events this month
    events_this_month = Event.objects.filter(date__year=year, date__month=month)
    events_by_day = {}
    for ev in events_this_month:
        events_by_day.setdefault(ev.date.day, []).append(ev)

    # Upcoming events (next 60 days) for list below grid
    upcoming = Event.objects.filter(date__gte=today, date__lte=today + timedelta(days=60)).order_by('date', 'start_time')

    # Previous / next month links
    prev_month = date(year, month, 1) - timedelta(days=1)
    next_month = date(year, month, 1) + timedelta(days=32)
    prev_month = prev_month.replace(day=1)
    next_month = next_month.replace(day=1)

    context = {
        'page_title':   'Event Calendar',
        'year':         year,
        'month':        month,
        'month_name':   month_name,
        'cal':          cal,
        'events_by_day': events_by_day,
        'today':        today,
        'upcoming':     upcoming,
        'prev_year':    prev_month.year,
        'prev_month':   prev_month.month,
        'next_year':    next_month.year,
        'next_month':   next_month.month,
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
