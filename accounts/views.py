from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    """
    Custom login view.
    - If user is already authenticated, redirect them to the portal.
    - POST: Authenticates credentials. On success, redirects musicians/admins
            to the portal dashboard; customers to home.
    - GET: Renders the login form.
    """
    if request.user.is_authenticated:
        return redirect('portal_dashboard')

    if request.GET.get('social_error'):
        messages.error(request, 'No account found for that Google email. Contact Gerry to get access.')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role in ('musician', 'admin'):
                return redirect('portal_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html', {'page_title': 'Login'})


def logout_view(request):
    """
    Logs the user out. Only accepts POST to prevent CSRF logout attacks
    (e.g. a malicious link that logs you out without your knowledge).
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
