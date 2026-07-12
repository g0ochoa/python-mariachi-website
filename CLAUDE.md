# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Website + private portal for Mariachi Todo Terreno, the owner's mariachi band. Public marketing site plus a musicians portal for gig scheduling, RSVP, a scores library, and per-gig musician pay tracking. Solo learning-focused project (owner is a security engineer); favor clear, working code over heavy process.

**Stack:** Django 5.2 with server-rendered templates (Bootstrap + Bootstrap Icons, vanilla JS, some HTMX-style partial endpoints). No DRF — views are function-based, reading `request.POST` directly (no Django forms for portal CRUD). SQLite locally, PostgreSQL in production (auto-switch: Postgres when `DB_NAME` env var is set — see `settings.py`).

## Commands

```bash
source venv-mac/bin/activate       # Mac dev venv (mariachi-env/ is stale — don't use)
python manage.py runserver         # dev server on :8000
python manage.py migrate
python manage.py makemigrations accounts musicians_portal public_site
python manage.py test              # test files are empty stubs — nothing real yet
```

Env vars load from a root `.env` (copy `.env.example`). Google integrations degrade gracefully when unset: `GOOGLE_ICAL_URL` (calendar read-sync), `GCAL_CALENDAR_ID` + `GCAL_SERVICE_ACCOUNT_JSON` (calendar write-back), `GOOGLE_OAUTH2_CLIENT_ID/SECRET` (SSO login).

There is no linter/formatter configured — match existing style (aligned `=` in model field blocks, section-divider comments in views.py).

### Deployment

Push to `main` → GitHub Actions (`.github/workflows/deploy-staging.yml`) rsyncs to a VPS, installs deps, migrates, runs collectstatic, and restarts the `mariachi-django` systemd (gunicorn) service. There is no separate production pipeline — main IS the deployed site. Config for the VPS lives in `deployment/` (nginx, gunicorn, systemd unit).

## Architecture

Three Django apps behind one URL conf (`mariachi_todo_terreno/urls.py`):

- **`accounts`** — custom user model `accounts.User` (`AUTH_USER_MODEL`) with a `role` field: `customer` / `musician` / `lead` / `admin`. Login is username/password or Google OAuth (social-auth); the custom pipeline step `accounts/pipeline.require_existing_account` blocks Google sign-in for any email without a pre-created account — there is no self-registration for the portal.
- **`public_site`** — homepage plus `SiteMedia`, a fixed-slot media registry (hero, gallery 1–6, video 1–4) editable at `/portal/media/`.
- **`musicians_portal`** — everything else; all logic lives in `musicians_portal/views.py` (~1,000 lines, function-based).

### Roles gate everything

Two helpers in `musicians_portal/views.py` define the permission model — use them, don't re-derive:
- `_require_portal(request)` — musician, lead, or admin may enter the portal (customers get 403).
- `_is_finance_user(user)` — **admin or lead only**: sees/edits event financials, musician pay, pay summary, event CRUD, gig logging, manual calendar sync.

Musician-specific `User` fields that drive the pay UI: `default_hourly_rate` (feeds Auto-Calculate), `instrument`, `is_test_account` (hidden from pay entry/summary), and `active_from`/`active_until` (a musician appears in an event's pay table only when the event date falls inside their active window).

### Event vs Gig — two different models

- `Event` (musicians_portal) is the calendar entity: gig/rehearsal/absence/other, date/times, venue, plus finance fields (`rate_per_hour`, `total_charged`, `billed_hours`, `is_paid`).
- `Gig` is a separate booking/CRM record (client name, event type like wedding/quinceañera, musician count) created only by the "Log New Gig" form (`gig_log`), which creates a `Gig` **and** a matching `Event` and pushes it to Google Calendar. They are not linked by FK — the Event is the operational record.

### Google Calendar sync (two directions, different mechanisms)

- **Read:** `_do_ical_sync` fetches the band calendar's iCal feed and `update_or_create`s Events keyed on `google_event_id`. It runs in a background thread on calendar page loads, at most every 30 min (Django cache key), or via the manual sync button. ⚠️ It **deletes** any Event whose `google_event_id` is non-empty but no longer in the feed — Events created in-app without a GCal id are safe, but never fabricate a `google_event_id`.
- **Write:** service-account API calls — `_push_to_gcal` (from gig logging), `_update_gcal` (on event edit), `_delete_gcal` (on delete). All fail soft with logging.

All datetimes normalize to `America/Chicago` (`BAND_TZ`).

### Musician pay flow (event detail page)

1. `event_detail` builds `all_musicians` (active, non-test, role in musician/lead/admin, active-window-filtered by event date) and attaches each one's existing `MusicianPay` amount/notes.
2. **Auto-Calculate** (client-side JS in `event_detail.html`) fills each row from `default_hourly_rate × hours`; lead/admin rows track manual overrides.
3. **Save All Pay** POSTs everything to `musician_pay_bulk`, which `get_or_create`s/updates one `MusicianPay` per non-empty amount — **this is when pay hits the DB**, not "Mark All as Paid".
4. **Mark All as Paid** (`mark_event_paid`) only flips `Event.is_paid` and bulk-sets `is_paid=True` on the event's existing MusicianPay rows. `musician_pay_bulk` keeps later-added rows in sync with an already-paid event.
5. `MusicianPay` is `unique_together (event, musician)` — one row per musician per event.

`pay_summary` renders a year-filtered pivot (events × musicians) built in Python from a single queryset; the paid/unpaid filter there means "client paid the band" (`Event.is_paid`), not per-musician payout status.

### Scores library

`Song` rows point at folders under `/var/www/mariachiesencia/scores/` (`SCORES_BASE_PATH`) — files are scanned from disk at request time (`_scan_song_folder`) and served from `mariachiesencia.com/scores/…`, not stored in Django media. On a dev machine that path doesn't exist, so song detail pages simply show no files.

### Financial dashboards

`_month_financial_stats` powers the calendar header: personal earned/owed/upcoming + YTD for every member; admin/lead additionally get band revenue aggregates from `Event.total_charged`/`is_paid`. "Owed" = unpaid with event date in the past; "upcoming" = unpaid, future-dated.
