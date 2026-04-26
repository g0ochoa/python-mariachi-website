from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ContactForm
from .models import SiteMedia


def home(request):
    """
    Home page view.
    - GET:  Renders home page with an empty contact form.
    - POST: Validates and saves the booking inquiry, then redirects
            back to home (Post-Redirect-Get pattern to prevent duplicate
            submissions on browser refresh).
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                '¡Gracias! We received your message and will contact you soon.'
            )
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'page_title': 'Home',
        'form': form,
    }
    return render(request, 'public_site/home.html', context)


# ─── Media Manager ───────────────────────────────────────────────────────────

# Human-friendly metadata for each slot used in the manager UI
SLOT_META = {
    'hero_image':  {'label': 'Hero Photo',        'type': 'image', 'hint': 'Main photo shown below the band name at the top of the homepage'},
    'about_image': {'label': 'About Photo',       'type': 'image', 'hint': 'Photo shown in the About / Our Story section'},
    'gallery_1':   {'label': 'Gallery 1',         'type': 'image', 'hint': 'Gallery grid — position 1'},
    'gallery_2':   {'label': 'Gallery 2',         'type': 'image', 'hint': 'Gallery grid — position 2'},
    'gallery_3':   {'label': 'Gallery 3',         'type': 'image', 'hint': 'Gallery grid — position 3'},
    'gallery_4':   {'label': 'Gallery 4',         'type': 'image', 'hint': 'Gallery grid — position 4'},
    'gallery_5':   {'label': 'Gallery 5',         'type': 'image', 'hint': 'Gallery grid — position 5'},
    'gallery_6':   {'label': 'Gallery 6',         'type': 'image', 'hint': 'Gallery grid — position 6'},
    'video_1':     {'label': 'Video Showcase 1',  'type': 'video', 'hint': 'First video in the homepage video player'},
    'video_2':     {'label': 'Video Showcase 2',  'type': 'video', 'hint': 'Second video'},
    'video_3':     {'label': 'Video Showcase 3',  'type': 'video', 'hint': 'Third video'},
    'video_4':     {'label': 'Video Showcase 4',  'type': 'video', 'hint': 'Fourth video'},
}


@login_required
def media_manager(request):
    if request.user.role != 'admin':
        messages.error(request, 'Admin access required.')
        return redirect('portal_dashboard')

    existing = {m.slot: m for m in SiteMedia.objects.all()}
    # Build slot list with current media attached
    slots = []
    for slot_key, meta in SLOT_META.items():
        slots.append({
            'key':     slot_key,
            'label':   meta['label'],
            'type':    meta['type'],
            'hint':    meta['hint'],
            'current': existing.get(slot_key),
        })

    return render(request, 'public_site/media_manager.html', {
        'slots': slots,
        'page_title': 'Media Manager',
    })


@login_required
@require_POST
def media_upload(request, slot):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Admin access required'}, status=403)

    if slot not in SLOT_META:
        return JsonResponse({'error': 'Unknown slot'}, status=400)

    uploaded = request.FILES.get('file')
    if not uploaded:
        messages.error(request, 'No file selected.')
        return redirect('media_manager')

    meta = SLOT_META[slot]
    media_type = meta['type']

    # Validate file type to prevent malicious uploads (OWASP: Unrestricted File Upload)
    IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
    VIDEO_TYPES = {'video/mp4', 'video/webm', 'video/ogg'}
    allowed = IMAGE_TYPES if media_type == 'image' else VIDEO_TYPES
    if uploaded.content_type not in allowed:
        messages.error(request, f'Invalid file type "{uploaded.content_type}" for {meta["label"]}.')
        return redirect('media_manager')

    obj, _ = SiteMedia.objects.get_or_create(slot=slot, defaults={'media_type': media_type})
    # Delete old file from disk before replacing
    if obj.file:
        obj.file.delete(save=False)
    obj.file = uploaded
    obj.media_type = media_type
    obj.alt_text = request.POST.get('alt_text', obj.alt_text)
    obj.caption = request.POST.get('caption', obj.caption)
    obj.save()

    messages.success(request, f'{meta["label"]} updated successfully.')
    return redirect('media_manager')


@login_required
@require_POST
def media_delete(request, slot):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Admin access required'}, status=403)

    obj = get_object_or_404(SiteMedia, slot=slot)
    obj.file.delete(save=False)
    obj.delete()
    messages.success(request, f'{SLOT_META.get(slot, {}).get("label", slot)} removed. The default static file will be shown.')
    return redirect('media_manager')
