from .models import SiteMedia


def site_media(request):
    """
    Injects all SiteMedia slots into every template as `site_media`.
    Usage in templates:
        {% if site_media.hero_image %}
            <img src="{{ site_media.hero_image.file.url }}" ...>
        {% endif %}
    """
    media_qs = SiteMedia.objects.all()
    media_map = {item.slot: item for item in media_qs}
    return {'site_media': media_map}
