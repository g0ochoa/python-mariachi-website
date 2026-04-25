from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


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
