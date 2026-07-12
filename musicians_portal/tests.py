from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Contract, ContractTemplate, Event, Gig, MusicianPay

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


class ContractTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='gerry', password='pw', role='admin', first_name='Gerry')
        self.musician = User.objects.create_user(
            username='juan', password='pw', role='musician', first_name='Juan')
        self.event = Event.objects.create(
            title='Sandra Vega', event_type='gig', date=date.today() + timedelta(days=30),
            client='Sandra Vega', total_charged=Decimal('650'))
        self.client.login(username='gerry', password='pw')

    def _create_contract(self, **overrides):
        data = {
            'client_name': 'Sandra Vega',
            'client_phone': '+14795551234',
            'client_email': 'sandra@example.com',
            'total_amount': '650',
            'deposit_amount': '150',
            'overtime_rate': '200',
            'contract_language': 'es',
        }
        data.update(overrides)
        return self.client.post(reverse('portal_contract_create', args=[self.event.id]), data)

    # ── setup / creation ────────────────────────────────────────────────

    def test_template_seeded_by_migration(self):
        self.assertTrue(ContractTemplate.objects.filter(is_active=True).exists())

    def test_gig_log_with_checkbox_creates_contract(self):
        resp = self.client.post(reverse('portal_gig_log'), {
            'client_name': 'Maria Lopez', 'client_phone': '+14795550000',
            'client_email': 'maria@example.com', 'event_type': 'wedding',
            'date': str(date.today() + timedelta(days=60)),
            'start_time': '18:00', 'end_time': '20:00',
            'venue': 'Amigos Event Center', 'city': 'Springdale, AR',
            'musicians_count': '6', 'total_charged': '1300',
            'deposit_amount': '300', 'overtime_rate': '250',
            'create_contract': 'on', 'contract_language': 'es',
        })
        contract = Contract.objects.get()
        self.assertRedirects(resp, reverse('portal_contract_detail', args=[contract.id]))
        self.assertEqual(contract.status, 'draft')
        self.assertEqual(contract.client_phone, '+14795550000')
        self.assertEqual(contract.deposit_amount, Decimal('300'))
        template = ContractTemplate.objects.get(is_active=True)
        self.assertEqual(contract.terms_es, template.terms_es)
        gig = Gig.objects.get()
        self.assertEqual(gig.client_phone, '+14795550000')
        self.assertEqual(gig.client_email, 'maria@example.com')
        self.assertEqual(contract.gig, gig)

    def test_gig_log_without_checkbox_creates_no_contract(self):
        self.client.post(reverse('portal_gig_log'), {
            'client_name': 'Maria Lopez', 'event_type': 'wedding',
            'date': str(date.today() + timedelta(days=60)),
            'start_time': '18:00', 'end_time': '20:00', 'musicians_count': '6',
        })
        self.assertFalse(Contract.objects.exists())

    def test_contract_create_from_event_detail(self):
        resp = self._create_contract()
        contract = Contract.objects.get()
        self.assertRedirects(resp, reverse('portal_contract_detail', args=[contract.id]))
        self.assertEqual(contract.event, self.event)
        self.assertEqual(contract.balance_due, Decimal('500'))

    def test_second_active_contract_blocked(self):
        self._create_contract()
        first = Contract.objects.get()
        resp = self._create_contract(client_name='Someone Else')
        self.assertRedirects(resp, reverse('portal_contract_detail', args=[first.id]))
        self.assertEqual(Contract.objects.count(), 1)

    def test_void_then_recreate_allowed(self):
        self._create_contract()
        first = Contract.objects.get()
        self.client.post(reverse('portal_contract_void', args=[first.id]))
        first.refresh_from_db()
        self.assertEqual(first.status, 'voided')
        self.assertIsNotNone(first.voided_at)
        self._create_contract()
        self.assertEqual(Contract.objects.count(), 2)

    def test_signed_snapshot_immune_to_template_edit(self):
        self._create_contract()
        contract = Contract.objects.get()
        original = contract.terms_es
        ContractTemplate.objects.filter(is_active=True).update(terms_es='NEW TERMS')
        contract.refresh_from_db()
        self.assertEqual(contract.terms_es, original)

    # ── permissions ─────────────────────────────────────────────────────

    def test_portal_contract_views_require_finance_role(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.logout()
        self.client.login(username='juan', password='pw')
        self.assertEqual(self.client.get(
            reverse('portal_contract_detail', args=[contract.id])).status_code, 403)
        self.assertEqual(self._create_contract().status_code, 403)
        self.assertEqual(self.client.post(
            reverse('portal_contract_void', args=[contract.id])).status_code, 403)

    # ── public signing page ─────────────────────────────────────────────

    def test_public_page_renders_without_login(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.logout()
        resp = self.client.get(reverse('contract_sign', args=[contract.token]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sandra Vega')
        self.assertContains(resp, 'lang-es')
        self.assertContains(resp, 'lang-en')
        self.assertEqual(resp['X-Robots-Tag'], 'noindex, nofollow')

    def test_unknown_token_404(self):
        import uuid
        resp = self.client.get(reverse('contract_sign', args=[uuid.uuid4()]))
        self.assertEqual(resp.status_code, 404)

    def test_signing_records_audit_fields(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.logout()
        url = reverse('contract_sign', args=[contract.token])
        resp = self.client.post(url, {'signed_name': 'Sandra Vega', 'agree': 'on', 'lang': 'es'},
                                HTTP_X_FORWARDED_FOR='203.0.113.9, 10.0.0.1',
                                HTTP_USER_AGENT='TestBrowser/1.0')
        self.assertRedirects(resp, url)
        contract.refresh_from_db()
        self.assertEqual(contract.status, 'signed')
        self.assertEqual(contract.signed_name, 'Sandra Vega')
        self.assertEqual(contract.signed_ip, '203.0.113.9')
        self.assertEqual(contract.signed_user_agent, 'TestBrowser/1.0')
        self.assertEqual(contract.signed_language, 'es')
        self.assertIsNotNone(contract.signed_at)
        confirm = self.client.get(url)
        self.assertContains(confirm, 'Sandra Vega')
        self.assertContains(confirm, 'Contract signed')

    def test_signing_idempotent(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.logout()
        url = reverse('contract_sign', args=[contract.token])
        self.client.post(url, {'signed_name': 'Sandra Vega', 'agree': 'on'})
        self.client.post(url, {'signed_name': 'Impostor', 'agree': 'on'})
        contract.refresh_from_db()
        self.assertEqual(contract.signed_name, 'Sandra Vega')

    def test_signing_requires_name_and_agree(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.logout()
        url = reverse('contract_sign', args=[contract.token])
        self.client.post(url, {'signed_name': '', 'agree': 'on'})
        self.client.post(url, {'signed_name': 'Sandra Vega'})
        contract.refresh_from_db()
        self.assertEqual(contract.status, 'draft')
        self.assertIsNone(contract.signed_at)

    def test_voided_contract_cannot_be_signed(self):
        self._create_contract()
        contract = Contract.objects.get()
        self.client.post(reverse('portal_contract_void', args=[contract.id]))
        self.client.logout()
        url = reverse('contract_sign', args=[contract.token])
        resp = self.client.get(url)
        self.assertContains(resp, 'no longer valid')
        self.client.post(url, {'signed_name': 'Sandra Vega', 'agree': 'on'})
        contract.refresh_from_db()
        self.assertEqual(contract.status, 'voided')
        self.assertIsNone(contract.signed_at)

    # ── sending ─────────────────────────────────────────────────────────

    def test_send_email_marks_sent(self):
        self._create_contract()
        contract = Contract.objects.get()
        resp = self.client.post(reverse('portal_contract_send_email', args=[contract.id]))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(str(contract.token), mail.outbox[0].body)
        contract.refresh_from_db()
        self.assertEqual(contract.status, 'sent')
        self.assertEqual(contract.sent_via, 'email')
        self.assertIn('sent=email', resp.url)

    def test_mark_sent_beacon(self):
        self._create_contract()
        contract = Contract.objects.get()
        resp = self.client.post(reverse('portal_contract_mark_sent', args=[contract.id]), {'via': 'sms'})
        self.assertEqual(resp.json(), {'ok': True})
        contract.refresh_from_db()
        self.assertEqual(contract.status, 'sent')
        self.assertEqual(contract.sent_via, 'sms')

    def test_twilio_button_hidden_when_unconfigured(self):
        self._create_contract()
        contract = Contract.objects.get()
        resp = self.client.get(reverse('portal_contract_detail', args=[contract.id]))
        self.assertNotContains(resp, 'Send SMS (Twilio)')
        with mock.patch.multiple('musicians_portal.views',
                                 TWILIO_ACCOUNT_SID='ACtest', TWILIO_AUTH_TOKEN='tok',
                                 TWILIO_FROM_NUMBER='+15005550006'):
            resp = self.client.get(reverse('portal_contract_detail', args=[contract.id]))
            self.assertContains(resp, 'Send SMS (Twilio)')

    def test_twilio_send_success_and_failure(self):
        self._create_contract()
        contract = Contract.objects.get()
        url = reverse('portal_contract_send_twilio', args=[contract.id])
        with mock.patch.multiple('musicians_portal.views',
                                 TWILIO_ACCOUNT_SID='ACtest', TWILIO_AUTH_TOKEN='tok',
                                 TWILIO_FROM_NUMBER='+15005550006'):
            with mock.patch('musicians_portal.views.http_requests.post') as mock_post:
                mock_post.return_value.status_code = 201
                resp = self.client.post(url)
                called_url = mock_post.call_args[0][0]
                self.assertIn('ACtest', called_url)
                self.assertEqual(mock_post.call_args[1]['auth'], ('ACtest', 'tok'))
                self.assertIn(str(contract.token), mock_post.call_args[1]['data']['Body'])
                self.assertIn('sent=twilio', resp.url)
            contract.refresh_from_db()
            self.assertEqual(contract.status, 'sent')
            self.assertEqual(contract.sent_via, 'twilio')

            # Failure path: a fresh contract stays draft on a 400
            contract2 = Contract.objects.create(
                event=Event.objects.create(title='X', event_type='gig',
                                           date=date.today() + timedelta(days=10)),
                client_name='B', client_phone='+15550001111',
                event_date=date.today() + timedelta(days=10),
                terms_en='t', terms_es='t')
            with mock.patch('musicians_portal.views.http_requests.post') as mock_post:
                mock_post.return_value.status_code = 400
                mock_post.return_value.text = 'bad request'
                resp = self.client.post(reverse('portal_contract_send_twilio', args=[contract2.id]))
                self.assertIn('err=twilio', resp.url)
            contract2.refresh_from_db()
            self.assertEqual(contract2.status, 'draft')
