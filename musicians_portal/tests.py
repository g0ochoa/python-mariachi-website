from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Event, MusicianPay

User = get_user_model()


class GuestMusicianTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='gerry', password='pw', role='admin', first_name='Gerry')
        self.musician = User.objects.create_user(
            username='juan', password='pw', role='musician', first_name='Juan')
        self.event = Event.objects.create(
            title='Quince', event_type='gig', date=date.today())
        self.later_event = Event.objects.create(
            title='Wedding', event_type='gig', date=date.today() + timedelta(days=14))
        self.client.login(username='gerry', password='pw')

    def _add_guest(self, **overrides):
        data = {
            'first_name': 'Ramiro',
            'last_name': 'Sub',
            'instrument': 'Guitarrón',
            'default_hourly_rate': '90',
        }
        data.update(overrides)
        return self.client.post(
            reverse('portal_guest_create', args=[self.event.id]), data)

    def test_guest_created_and_appears_on_event(self):
        resp = self._add_guest()
        self.assertRedirects(resp, reverse('portal_event_detail', args=[self.event.id]))
        guest = User.objects.get(is_guest=True)
        self.assertEqual(guest.username, 'guest-ramiro-sub')
        self.assertEqual(guest.role, 'musician')
        self.assertEqual(guest.active_from, self.event.date)
        self.assertIsNone(guest.active_until)
        self.assertFalse(guest.has_usable_password())

        detail = self.client.get(reverse('portal_event_detail', args=[self.event.id]))
        self.assertIn(guest, detail.context['all_musicians'])
        self.assertContains(detail, 'guest-deact-%d' % guest.id)

    def test_guest_appears_on_later_events_until_deactivated(self):
        self._add_guest()
        guest = User.objects.get(is_guest=True)

        later = self.client.get(reverse('portal_event_detail', args=[self.later_event.id]))
        self.assertIn(guest, later.context['all_musicians'])

        self.client.post(reverse('portal_guest_deactivate', args=[self.event.id, guest.id]))
        guest.refresh_from_db()
        self.assertEqual(guest.active_until, self.event.date)

        later = self.client.get(reverse('portal_event_detail', args=[self.later_event.id]))
        self.assertNotIn(guest, later.context['all_musicians'])
        # Still on the original event (window includes its date)
        original = self.client.get(reverse('portal_event_detail', args=[self.event.id]))
        self.assertIn(guest, original.context['all_musicians'])

    def test_username_collision_gets_suffix(self):
        self._add_guest()
        self._add_guest()
        usernames = set(User.objects.filter(is_guest=True).values_list('username', flat=True))
        self.assertEqual(usernames, {'guest-ramiro-sub', 'guest-ramiro-sub-2'})

    def test_guest_pay_flows_through_bulk_save(self):
        self._add_guest()
        guest = User.objects.get(is_guest=True)
        self.client.post(
            reverse('portal_musician_pay_bulk', args=[self.event.id]),
            {f'amount_{guest.id}': '90', f'notes_{guest.id}': 'cash'})
        pay = MusicianPay.objects.get(event=self.event, musician=guest)
        self.assertEqual(pay.amount, Decimal('90'))
        self.assertFalse(pay.is_paid)

    def test_deactivate_rejects_non_guests(self):
        resp = self.client.post(
            reverse('portal_guest_deactivate', args=[self.event.id, self.musician.id]))
        self.assertEqual(resp.status_code, 404)
        self.musician.refresh_from_db()
        self.assertIsNone(self.musician.active_until)

    def test_requires_finance_role(self):
        self.client.logout()
        self.client.login(username='juan', password='pw')
        resp = self._add_guest()
        self.assertEqual(resp.status_code, 403)

    def test_blank_first_name_creates_nothing(self):
        self._add_guest(first_name='')
        self.assertFalse(User.objects.filter(is_guest=True).exists())
