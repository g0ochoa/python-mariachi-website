import os
from urllib.parse import quote

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Song

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
