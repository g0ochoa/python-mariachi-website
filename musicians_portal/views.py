from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Song


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

    query      = request.GET.get('q', '').strip()
    genre      = request.GET.get('genre', '')
    difficulty = request.GET.get('difficulty', '')
    has_audio  = request.GET.get('has_audio', '')

    songs = Song.objects.filter(is_active=True)

    if query:
        songs = songs.filter(Q(title__icontains=query) | Q(folder_name__icontains=query))
    if genre:
        songs = songs.filter(genre=genre)
    if difficulty:
        songs = songs.filter(difficulty=difficulty)
    if has_audio == '1':
        songs = songs.filter(has_audio=True)

    context = {
        'page_title': 'Scores Library',
        'songs':      songs,
        'total':      Song.objects.filter(is_active=True).count(),
        'query':      query,
        'genre':      genre,
        'difficulty': difficulty,
        'has_audio':  has_audio,
        'genres':     Song.GENRE_CHOICES,
        'difficulties': Song.DIFFICULTY_CHOICES,
    }
    return render(request, 'musicians_portal/scores.html', context)
