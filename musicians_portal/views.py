import os
import calendar
import logging
import threading
from datetime import date, datetime, timedelta
from django.utils import timezone
from urllib.parse import quote
from zoneinfo import ZoneInfo

import requests as http_requests
from icalendar import Calendar as iCalendar

BAND_TZ = ZoneInfo('America/Chicago')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum, Case, When, DecimalField
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Song, Event, EventAttendance, Gig, MusicianPay

GCAL_SYNC_CACHE_KEY    = 'gcal_last_sync'
GCAL_SYNC_INTERVAL     = 30 * 60   # seconds — re-sync at most every 30 minutes

GOOGLE_ICAL_URL              = os.environ.get('GOOGLE_ICAL_URL', '')
GCAL_CALENDAR_ID             = os.environ.get('GCAL_CALENDAR_ID', '')
GCAL_SERVICE_ACCOUNT_JSON    = os.environ.get('GCAL_SERVICE_ACCOUNT_JSON', '')


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
            event_end_date = None  # single-day timed event
        else:
            end_time = None
            # iCal all-day DTEND is exclusive — subtract 1 day for the actual last day
            last_day = dtend_val - timedelta(days=1)
            event_end_date = last_day if last_day > event_date else None

        location    = str(component.get('LOCATION',    '') or '').strip()
        description = str(component.get('DESCRIPTION', '') or '').strip()

        seen_uids.add(uid)

        defaults = {
            'title':      summary[:200],
            'event_type': _detect_event_type(summary),
            'date':       event_date,
            'end_date':   event_end_date,
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


def _build_week_events(cal, year, month, events_by_day):
    """
    For each week in `cal`, return a list of event-span dicts for CSS Grid rendering.
    Each dict: {event, col_start (1-7), col_span (1+), continues_from, continues_after}
    Multi-day events spanning a week boundary appear in both affected weeks, clamped.
    """
    from datetime import date as date_cls
    week_events = []
    for week in cal:
        col_dates = {ci: date_cls(year, month, d) for ci, d in enumerate(week) if d != 0}
        if not col_dates:
            week_events.append([])
            continue
        week_start = min(col_dates.values())
        week_end   = max(col_dates.values())
        seen_ids = set()
        spans = []
        for col_idx in sorted(col_dates):
            day_num = week[col_idx]
            for ev in events_by_day.get(day_num, []):
                if ev.id in seen_ids:
                    continue
                seen_ids.add(ev.id)
                ev_end = ev.end_date if ev.end_date else ev.date
                clamp_start = max(ev.date, week_start)
                clamp_end   = min(ev_end, week_end)
                # Find CSS grid column numbers (1-indexed)
                start_col = end_col = None
                for ci, d in col_dates.items():
                    if d == clamp_start:
                        start_col = ci + 1
                    if d == clamp_end:
                        end_col = ci + 1
                if start_col is None or end_col is None:
                    continue
                spans.append({
                    'event':           ev,
                    'col_start':       start_col,
                    'col_span':        end_col - start_col + 1,
                    'continues_from':  ev.date < week_start,
                    'continues_after': ev_end > week_end,
                })
        week_events.append(spans)
    return week_events


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
    if request.user.role not in ('musician', 'lead', 'admin'):
        raise PermissionDenied

    context = {
        'page_title': 'Musicians Portal',
    }
    return render(request, 'musicians_portal/dashboard.html', context)


@login_required
def scores(request):
    if request.user.role not in ('musician', 'lead', 'admin'):
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
    if request.user.role not in ('musician', 'lead', 'admin'):
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
    """Raise PermissionDenied if user is not musician, lead, or admin."""
    if request.user.role not in ('musician', 'lead', 'admin'):
        raise PermissionDenied


def _is_finance_user(user):
    """Returns True for users who can see/edit financial data."""
    return user.role in ('admin', 'lead')


def _month_financial_stats(user, year, month, today):
    """Compute monthly and YTD financial stats.
    Admin/lead get personal + business totals.
    Musicians get personal totals only.
    Returns None for customers."""
    if user.role not in ('admin', 'lead', 'musician'):
        return None
    is_finance = user.role in ('admin', 'lead')
    jan_first = date(today.year, 1, 1)

    # Single query: earned, owed (played but unpaid), upcoming (future, unpaid)
    personal_month = MusicianPay.objects.filter(
        musician=user,
        event__date__year=year,
        event__date__month=month,
    ).aggregate(
        earned=Sum(Case(When(is_paid=True, then='amount'), output_field=DecimalField())),
        owed=Sum(Case(When(is_paid=False, event__date__lte=today, then='amount'), output_field=DecimalField())),
        upcoming=Sum(Case(When(is_paid=False, event__date__gt=today, then='amount'), output_field=DecimalField())),
    )
    my_earned   = personal_month['earned']   or 0
    my_owed     = personal_month['owed']     or 0
    my_upcoming = personal_month['upcoming'] or 0

    # Single query for YTD
    my_ytd = MusicianPay.objects.filter(
        musician=user,
        event__date__gte=jan_first,
        event__date__lte=today,
        is_paid=True,
    ).aggregate(t=Sum('amount'))['t'] or 0

    result = {
        'is_finance': is_finance,
        'my_earned':  my_earned,
        'my_owed':    my_owed,
        'my_upcoming': my_upcoming,
        'my_ytd':     my_ytd,
    }

    if is_finance:
        # Single query: earned, owed, upcoming for band revenue this month
        biz_month = Event.objects.filter(
            date__year=year, date__month=month,
            total_charged__isnull=False,
        ).aggregate(
            earned=Sum(Case(When(is_paid=True, then='total_charged'), output_field=DecimalField())),
            owed=Sum(Case(When(is_paid=False, date__lte=today, then='total_charged'), output_field=DecimalField())),
            upcoming=Sum(Case(When(is_paid=False, date__gt=today, then='total_charged'), output_field=DecimalField())),
        )
        biz_earned   = biz_month['earned']   or 0
        biz_owed     = biz_month['owed']     or 0
        biz_upcoming = biz_month['upcoming'] or 0

        biz_ytd = Event.objects.filter(
            date__gte=jan_first,
            date__lte=today,
            is_paid=True,
            total_charged__isnull=False,
        ).aggregate(t=Sum('total_charged'))['t'] or 0

        result['biz_earned']   = biz_earned
        result['biz_owed']     = biz_owed
        result['biz_upcoming'] = biz_upcoming
        result['biz_ytd']      = biz_ytd

    return result


@login_required
def calendar_month_partial(request):
    """Returns just the calendar grid HTML fragment for AJAX month navigation."""
    _require_portal(request)
    today = timezone.localdate()
    year  = int(request.GET.get('year',  today.year))
    month = int(request.GET.get('month', today.month))
    if month < 1:  month = 12; year -= 1
    if month > 12: month = 1;  year += 1

    cal        = calendar.monthcalendar(year, month)
    month_name = date(year, month, 1).strftime('%B %Y')

    first_day = date(year, month, 1)
    last_day  = date(year, month, calendar.monthrange(year, month)[1])

    # Events that overlap this month (single-day or spanning)
    events_this_month = Event.objects.filter(
        Q(date__lte=last_day) & (Q(end_date__isnull=True, date__gte=first_day) | Q(end_date__gte=first_day))
    )
    events_by_day = {}
    for ev in events_this_month:
        span_end = ev.end_date if ev.end_date else ev.date
        cur = max(ev.date, first_day)
        while cur <= min(span_end, last_day):
            events_by_day.setdefault(cur.day, []).append(ev)
            cur += timedelta(days=1)

    prev_month = (date(year, month, 1) - timedelta(days=1)).replace(day=1)
    next_month = (date(year, month, 1) + timedelta(days=32)).replace(day=1)

    gig_count = sum(1 for ev in events_this_month if ev.event_type == 'gig')
    gig_ids = [ev.id for ev in events_this_month if ev.event_type == 'gig']
    gigs_with_pay = 0
    if _is_finance_user(request.user) and gig_ids:
        gigs_with_pay = MusicianPay.objects.filter(
            event_id__in=gig_ids
        ).values('event_id').distinct().count()
    week_events = _build_week_events(cal, year, month, events_by_day)
    cal_weeks = [{'days': w, 'event_spans': we} for w, we in zip(cal, week_events)]

    context = {
        'year': year, 'month': month, 'month_name': month_name,
        'cal': cal, 'cal_weeks': cal_weeks, 'events_by_day': events_by_day, 'today': today,
        'prev_year': prev_month.year, 'prev_month': prev_month.month,
        'next_year': next_month.year, 'next_month': next_month.month,
        'gig_count': gig_count,
        'gigs_with_pay': gigs_with_pay,
        'month_stats': _month_financial_stats(request.user, year, month, today),
    }
    return render(request, 'musicians_portal/partials/calendar_month.html', context)


@login_required
def event_calendar(request):
    _require_portal(request)

    today = timezone.localdate()
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

    first_day = date(year, month, 1)
    last_day  = date(year, month, calendar.monthrange(year, month)[1])

    # All events that overlap this month (handles multi-day spans)
    events_this_month = Event.objects.filter(
        Q(date__lte=last_day) & (Q(end_date__isnull=True, date__gte=first_day) | Q(end_date__gte=first_day))
    )
    events_by_day = {}
    for ev in events_this_month:
        span_end = ev.end_date if ev.end_date else ev.date
        cur = max(ev.date, first_day)
        while cur <= min(span_end, last_day):
            events_by_day.setdefault(cur.day, []).append(ev)
            cur += timedelta(days=1)

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

    gig_count = sum(1 for ev in events_this_month if ev.event_type == 'gig')
    gig_ids = [ev.id for ev in events_this_month if ev.event_type == 'gig']
    gigs_with_pay = 0
    if _is_finance_user(request.user) and gig_ids:
        gigs_with_pay = MusicianPay.objects.filter(
            event_id__in=gig_ids
        ).values('event_id').distinct().count()
    week_events = _build_week_events(cal, year, month, events_by_day)
    cal_weeks = [{'days': w, 'event_spans': we} for w, we in zip(cal, week_events)]

    context = {
        'page_title':    'Event Calendar',
        'year':          year,
        'month':         month,
        'month_name':    month_name,
        'cal':           cal,
        'cal_weeks':     cal_weeks,
        'events_by_day': events_by_day,
        'today':         today,
        'upcoming':      upcoming,
        'next_up':       upcoming[:3],
        'user_rsvp':     user_rsvp,
        'prev_year':     prev_month.year,
        'prev_month':    prev_month.month,
        'next_year':     next_month.year,
        'next_month':    next_month.month,
        'gig_count':     gig_count,
        'gigs_with_pay': gigs_with_pay,
        'month_stats':   _month_financial_stats(request.user, year, month, today),
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

    # Finance data (only queried when user has access)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    pay_records    = []
    all_musicians  = []
    pay_map        = {}   # musician_id -> {'amount': ..., 'notes': ...}
    event_hours    = None
    if _is_finance_user(request.user):
        pay_records   = MusicianPay.objects.filter(event=event).select_related('musician')
        pay_map       = {p.musician_id: {'amount': p.amount, 'notes': p.notes} for p in pay_records}
        all_musicians = list(
            User.objects.filter(
                role__in=['musician', 'lead', 'admin'],
                is_test_account=False,
            ).filter(
                # active_from: not set, or on/before the event date
                Q(active_from__isnull=True) | Q(active_from__lte=event.date)
            ).filter(
                # active_until: not set, or on/after the event date
                Q(active_until__isnull=True) | Q(active_until__gte=event.date)
            ).order_by('first_name', 'username')
        )
        # Attach existing pay data directly to each musician for easy template access
        for m in all_musicians:
            pm = pay_map.get(m.id)
            m.pay_amount = pm['amount'] if pm else ''
            m.pay_notes  = pm['notes']  if pm else ''
        if event.billed_hours:
            event_hours = float(event.billed_hours)
        elif event.start_time and event.end_time:
            from datetime import datetime, date as _date, timedelta as _td
            _start = datetime.combine(_date.today(), event.start_time)
            _end   = datetime.combine(_date.today(), event.end_time)
            if _end < _start:
                _end += _td(days=1)
            event_hours = round((_end - _start).total_seconds() / 3600, 2)

    context = {
        'page_title':     event.title,
        'event':          event,
        'attendance':     attendance,
        'all_attendance': all_attendance,
        'pay_records':    pay_records,
        'all_musicians':  all_musicians,
        'pay_map':        pay_map,
        'event_hours':    event_hours,
        'is_finance_user': _is_finance_user(request.user),
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
    if not _is_finance_user(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        p = request.POST
        event_type = p.get('event_type', 'gig')
        is_absence = event_type == 'absence'
        event = Event.objects.create(
            title         = p['title'],
            event_type    = event_type,
            date          = p['date'],
            end_date      = p.get('end_date') or None,
            start_time    = p.get('start_time') or None,
            end_time      = p.get('end_time')   or None,
            venue         = p.get('venue', ''),
            client        = p.get('client', ''),
            notes         = p.get('notes', ''),
            rate_per_hour = None if is_absence else (p.get('rate_per_hour') or None),
            total_charged = None if is_absence else (p.get('total_charged') or None),
            billed_hours  = None if is_absence else (p.get('billed_hours')  or None),
            created_by    = request.user,
        )
        return redirect('portal_event_detail', event_id=event.id)

    context = {'page_title': 'Add Event'}
    return render(request, 'musicians_portal/event_form.html', context)


@login_required
def event_edit(request, event_id):
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        p = request.POST
        event_type = p.get('event_type', 'gig')
        is_absence = event_type == 'absence'
        event.title         = p['title']
        event.event_type    = event_type
        event.date          = p['date']
        event.end_date      = p.get('end_date') or None
        event.start_time    = p.get('start_time') or None
        event.end_time      = p.get('end_time')   or None
        event.venue         = p.get('venue', '')
        event.client        = p.get('client', '')
        event.notes         = p.get('notes', '')
        event.rate_per_hour = None if is_absence else (p.get('rate_per_hour') or None)
        event.total_charged = None if is_absence else (p.get('total_charged') or None)
        event.billed_hours  = None if is_absence else (p.get('billed_hours')  or None)
        event.save()
        _update_gcal(event)
        return redirect('portal_event_detail', event_id=event.id)

    context = {'page_title': 'Edit Event', 'event': event}
    return render(request, 'musicians_portal/event_form.html', context)


@login_required
@require_POST
def event_delete(request, event_id):
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)
    year, month = event.date.year, event.date.month
    gcal_id = event.google_event_id
    event.delete()
    _delete_gcal(gcal_id)
    return redirect(f'/portal/calendar/?year={year}&month={month}')


@login_required
@require_POST
def sync_google_calendar(request):
    """Force a manual sync (admin only), bypassing the cache cooldown."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    cache.delete(GCAL_SYNC_CACHE_KEY)
    result = _do_ical_sync()
    if result is None:
        return JsonResponse({'error': 'GOOGLE_ICAL_URL not configured'}, status=502)
    created, updated, deleted = result
    return JsonResponse({'created': created, 'updated': updated, 'deleted': deleted})


# ---------------------------------------------------------------------------
# Google Calendar write-back
# ---------------------------------------------------------------------------

def _gcal_service():
    """Build and return an authenticated Google Calendar service, or None."""
    if not GCAL_SERVICE_ACCOUNT_JSON or not GCAL_CALENDAR_ID:
        return None
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        credentials = service_account.Credentials.from_service_account_file(
            GCAL_SERVICE_ACCOUNT_JSON,
            scopes=['https://www.googleapis.com/auth/calendar.events'],
        )
        return build('calendar', 'v3', credentials=credentials)
    except Exception as exc:
        logging.getLogger(__name__).error('GCal auth failed: %s', exc)
        return None


def _push_to_gcal(gig, title):
    """Create an event in Google Calendar. Returns the GCal event ID or None."""
    logger = logging.getLogger(__name__)

    service = _gcal_service()
    if not service:
        logger.warning('GCal write skipped: credentials not configured')
        return None

    try:
        tz       = 'America/Chicago'
        location = ', '.join(filter(None, [gig.venue, gig.city]))
        gig_date = gig.date if isinstance(gig.date, date) else date.fromisoformat(str(gig.date))
        start_dt = datetime.combine(gig_date, gig.start_time).isoformat()
        end_dt   = datetime.combine(gig_date, gig.end_time).isoformat()

        body = {
            'summary':     title,
            'location':    location,
            'description': gig.notes,
            'start':       {'dateTime': start_dt, 'timeZone': tz},
            'end':         {'dateTime': end_dt,   'timeZone': tz},
        }

        result = service.events().insert(calendarId=GCAL_CALENDAR_ID, body=body).execute()
        return result.get('id')
    except Exception as exc:
        logging.getLogger(__name__).error('GCal push failed: %s', exc)
        return None


def _update_gcal(event):
    """Update an existing GCal event to match the Django Event. No-op if no google_event_id."""
    logger = logging.getLogger(__name__)

    if not event.google_event_id:
        return
    service = _gcal_service()
    if not service:
        return
    try:
        tz       = 'America/Chicago'
        location = ', '.join(filter(None, [event.venue or '', event.city if hasattr(event, 'city') else '']))
        ev_date  = event.date if isinstance(event.date, date) else date.fromisoformat(str(event.date))

        body = {'summary': event.title, 'location': location, 'description': event.notes or ''}
        if event.start_time and event.end_time:
            body['start'] = {'dateTime': datetime.combine(ev_date, event.start_time).isoformat(), 'timeZone': tz}
            body['end']   = {'dateTime': datetime.combine(ev_date, event.end_time).isoformat(),   'timeZone': tz}
        else:
            body['start'] = {'date': ev_date.isoformat()}
            body['end']   = {'date': ev_date.isoformat()}

        service.events().update(
            calendarId=GCAL_CALENDAR_ID,
            eventId=event.google_event_id,
            body=body,
        ).execute()
        logger.info('GCal event updated: %s', event.google_event_id)
    except Exception as exc:
        logger.error('GCal update failed: %s', exc)


def _delete_gcal(google_event_id):
    """Delete a GCal event by its event ID. No-op if id is blank."""
    logger = logging.getLogger(__name__)

    if not google_event_id:
        return
    service = _gcal_service()
    if not service:
        return
    try:
        service.events().delete(calendarId=GCAL_CALENDAR_ID, eventId=google_event_id).execute()
        logger.info('GCal event deleted: %s', google_event_id)
    except Exception as exc:
        logger.error('GCal delete failed: %s', exc)


# ---------------------------------------------------------------------------
# Log New Gig (admin only) — creates Gig + Event + GCal event
# ---------------------------------------------------------------------------

@login_required
def gig_log(request):
    """Admin/lead form to log a new gig: creates Gig record, Event for the
    calendar, and pushes the event to Google Calendar."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        p = request.POST

        client_name     = p.get('client_name', '').strip()
        event_type      = p.get('event_type', 'private')
        date_val        = p.get('date', '')
        start_time_val  = p.get('start_time') or None
        end_time_val    = p.get('end_time')   or None
        venue           = p.get('venue', '').strip()
        city            = p.get('city', '').strip()
        musicians_count = int(p.get('musicians_count') or 1)
        rate_per_hour   = p.get('rate_per_hour')  or None
        total_charged   = p.get('total_charged')  or None
        notes           = p.get('notes', '').strip()

        gig = Gig.objects.create(
            client_name     = client_name,
            event_type      = event_type,
            date            = date_val,
            start_time      = start_time_val,
            end_time        = end_time_val,
            venue           = venue,
            city            = city,
            musicians_count = musicians_count,
            rate_per_hour   = rate_per_hour,
            total_charged   = total_charged,
            notes           = notes,
        )

        # Calendar event title uses client name so it matches existing Google Cal style
        event_title = client_name
        event = Event.objects.create(
            title         = event_title,
            event_type    = 'gig',
            date          = date_val,
            start_time    = start_time_val,
            end_time      = end_time_val,
            venue         = venue,
            notes         = notes,
            rate_per_hour = rate_per_hour,
            total_charged = total_charged,
            created_by    = request.user,
        )

        # Push to Google Calendar and store the GCal event ID
        gcal_id = _push_to_gcal(gig, event_title)
        if gcal_id:
            event.google_event_id = gcal_id
            event.save()

        return redirect('portal_event_detail', event_id=event.id)

    context = {
        'page_title':   'Log New Gig',
        'event_types':  Gig.EVENT_TYPE_CHOICES,
        'gcal_ready':   bool(GCAL_SERVICE_ACCOUNT_JSON and GCAL_CALENDAR_ID),
    }
    return render(request, 'musicians_portal/gig_log_form.html', context)


# ---------------------------------------------------------------------------
# Musician Pay
# ---------------------------------------------------------------------------

@login_required
@require_POST
def musician_pay_set(request, event_id):
    """Create or update a MusicianPay record for a musician on an event."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    event      = get_object_or_404(Event, id=event_id)
    musician_id = request.POST.get('musician_id')
    amount      = request.POST.get('amount', '').strip()
    notes       = request.POST.get('notes', '').strip()

    if not musician_id or not amount:
        return redirect('portal_event_detail', event_id=event_id)

    from django.contrib.auth import get_user_model
    User = get_user_model()
    musician = get_object_or_404(User, id=musician_id)

    pay, created = MusicianPay.objects.get_or_create(
        event=event,
        musician=musician,
        defaults={'amount': amount, 'notes': notes, 'created_by': request.user},
    )
    if not created:
        pay.amount = amount
        pay.notes  = notes
        pay.save()

    return redirect('portal_event_detail', event_id=event_id)


@login_required
@require_POST
def musician_pay_bulk(request, event_id):
    """Bulk create/update MusicianPay records for all musicians on an event."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)

    from django.contrib.auth import get_user_model
    User = get_user_model()
    musicians = User.objects.filter(role__in=['musician', 'lead', 'admin'])

    for musician in musicians:
        amount_str = request.POST.get(f'amount_{musician.id}', '').strip()
        notes_str  = request.POST.get(f'notes_{musician.id}', '').strip()

        if not amount_str:
            continue
        try:
            amount = float(amount_str)
        except ValueError:
            continue
        if amount < 0:
            continue

        pay, created = MusicianPay.objects.get_or_create(
            event=event,
            musician=musician,
            defaults={
                'amount': amount,
                'notes': notes_str,
                'created_by': request.user,
                'is_paid': event.is_paid,  # inherit event paid status
            },
        )
        if not created:
            pay.amount = amount
            pay.notes  = notes_str
            if event.is_paid:
                pay.is_paid = True  # keep in sync if event already marked paid
            pay.save()

    # If event is already marked paid, ensure ALL pay records are in sync
    # (catches records that existed before mark_event_paid was called)
    if event.is_paid:
        MusicianPay.objects.filter(event=event).update(is_paid=True)

    return redirect('portal_event_detail', event_id=event_id)


@login_required
@require_POST
def mark_event_paid(request, event_id):
    """Mark all MusicianPay records for an event as is_paid=True and set Event.is_paid=True."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    event = get_object_or_404(Event, id=event_id)
    event.is_paid = True
    event.save(update_fields=['is_paid'])
    MusicianPay.objects.filter(event=event).update(is_paid=True)

    return redirect('portal_event_detail', event_id=event_id)


@login_required
def pay_summary(request):
    """Consolidated pay summary — pivot table of events × musicians."""
    _require_portal(request)
    if not _is_finance_user(request.user):
        raise PermissionDenied

    from decimal import Decimal
    from collections import defaultdict
    from django.contrib.auth import get_user_model
    User = get_user_model()

    selected_year         = int(request.GET.get('year', date.today().year))
    selected_musician_ids = request.GET.getlist('musician')   # multi-value list
    date_from             = request.GET.get('date_from', '').strip()
    date_to               = request.GET.get('date_to', '').strip()
    paid_filter           = request.GET.get('paid', '')        # '' | 'paid' | 'unpaid'

    # Year dropdown
    available_years = (
        MusicianPay.objects
        .filter(event__date__isnull=False)
        .dates('event__date', 'year')
    )
    year_list = sorted({d.year for d in available_years}, reverse=True)
    if selected_year not in year_list:
        year_list = [selected_year] + year_list

    # Base queryset for selected year
    pays_qs = (
        MusicianPay.objects
        .filter(event__date__year=selected_year)
        .select_related('musician', 'event')
        .order_by('event__date', 'event__start_time', 'musician__first_name')
    )

    # Date range
    if date_from:
        pays_qs = pays_qs.filter(event__date__gte=date_from)
    if date_to:
        pays_qs = pays_qs.filter(event__date__lte=date_to)

    # Paid / unpaid (based on Event.is_paid — whether client paid the band)
    if paid_filter == 'paid':
        pays_qs = pays_qs.filter(event__is_paid=True)
    elif paid_filter == 'unpaid':
        pays_qs = pays_qs.filter(event__is_paid=False)

    # All musicians who have pay records this year (for filter UI)
    musician_list = list(
        User.objects.filter(
            id__in=MusicianPay.objects
            .filter(event__date__year=selected_year)
            .values_list('musician_id', flat=True)
        ).order_by('first_name', 'username')
    )

    # Build pivot: event_id → {musician_id → MusicianPay}
    event_pay_map = defaultdict(dict)
    events_map    = {}
    for pay in pays_qs:
        event_pay_map[pay.event_id][pay.musician_id] = pay
        events_map[pay.event_id] = pay.event

    # Musician columns — respect multi-select filter
    if selected_musician_ids:
        col_ids          = set(selected_musician_ids)
        musician_columns = [m for m in musician_list if str(m.id) in col_ids]
    else:
        present_ids      = set()
        for pays in event_pay_map.values():
            present_ids.update(pays.keys())
        musician_columns = [m for m in musician_list if m.id in present_ids]

    # Build ordered event rows (date asc)
    sorted_events = sorted(events_map.values(), key=lambda e: (e.date, e.start_time or date.min))
    event_rows = []
    for event in sorted_events:
        row_pays = event_pay_map[event.id]
        event_rows.append({
            'event':         event,
            'musician_pays': [row_pays.get(m.id) for m in musician_columns],
        })

    # Per-musician column totals
    musician_totals = [
        sum(
            (row['musician_pays'][i].amount for row in event_rows if row['musician_pays'][i]),
            Decimal('0')
        )
        for i, _ in enumerate(musician_columns)
    ]

    context = {
        'page_title':             f'Pay Summary {selected_year}',
        'event_rows':             event_rows,
        'musician_columns':       musician_columns,
        'musician_totals':        musician_totals,
        'musician_list':          musician_list,
        'selected_year':          selected_year,
        'year_list':              year_list,
        'selected_musician_ids':  selected_musician_ids,
        'date_from':              date_from,
        'date_to':                date_to,
        'paid_filter':            paid_filter,
    }
    return render(request, 'musicians_portal/pay_summary.html', context)
