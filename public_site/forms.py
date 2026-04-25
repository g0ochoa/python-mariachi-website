from django import forms
from .models import BookingRequest


class ContactForm(forms.ModelForm):
    """
    ModelForm backed by BookingRequest — every valid submission is saved
    directly to the database so Gerry can review inquiries in the admin panel.
    """
    class Meta:
        model = BookingRequest
        fields = ['name', 'email', 'phone', 'event_type', 'message', 'promo_opt_in']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567',
            }),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your event...',
            }),
            'promo_opt_in': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'event_type': 'Event Type',
            'message': 'Message',
            'promo_opt_in': "I'd like to receive updates and promotional offers",
        }
