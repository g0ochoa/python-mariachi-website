from social_core.exceptions import AuthForbidden
from .models import User


def require_existing_account(backend, details, user=None, *args, **kwargs):
    """
    Custom social-auth pipeline step.
    Blocks Google login for any email that doesn't have a pre-existing account.
    Musicians and admins must be created by the admin first; they cannot
    self-register via Google.
    """
    if user:
        # Already matched to an existing user by social_user step — allow through.
        return

    email = details.get('email', '').lower().strip()
    if not email:
        raise AuthForbidden(backend)

    try:
        existing = User.objects.get(email__iexact=email)
        # Return the matched user so associate_by_email can link the social account.
        return {'user': existing}
    except User.DoesNotExist:
        raise AuthForbidden(backend)
