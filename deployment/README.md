# Deployment — how it actually works

> This repo is **public** — server usernames, paths, and IPs are deliberately not
> written here. The real values live in GitHub Actions variables/secrets
> (`gh variable list`): `STAGING_HOST`, `STAGING_USER`, `STAGING_PROJECT_PATH`,
> and the `STAGING_SSH_KEY` secret.

## Pipeline

Every push to `main` runs `.github/workflows/deploy-staging.yml`:

1. rsync the repo to `<STAGING_PROJECT_PATH>` on the VPS (`--delete` — files
   removed from the repo are removed from the server too).
2. `pip install -r requirements.txt` into the server's `venv/`.
3. `manage.py migrate --noinput`
4. `manage.py collectstatic` → copied to `/var/www/mariachi-django-static/`
5. `sudo systemctl restart mariachi-django`

There is no separate production pipeline — `main` is the live site.

## Server layout (for orientation; owned by the VPS, not this repo)

- **systemd**: `/etc/systemd/system/mariachi-django.service` — runs gunicorn
  (3 workers, bind `127.0.0.1:8000`, logs in `/var/log/mariachi-django/`),
  loads env from the project's `.env` on the server.
- **nginx** (`/etc/nginx/sites-enabled/`): two sites proxy to the same gunicorn:
  - `mariachitodoterreno.com` — the customer-facing site.
  - `mariachiesencia.com` — same Django app, plus `/scores/` (static score
    files at `/var/www/mariachi-esencia/scores/`, autoindex, used by the
    portal's scores library) and a legacy PHP API.
  - Both serve `/django-static/` from `/var/www/mariachi-django-static/` and
    `/site-media/` from the project's `media/` directory. TLS via Let's Encrypt.
- **Database**: PostgreSQL on the same box (Django auto-selects Postgres when
  `DB_NAME` is set in `.env` — see `mariachi_todo_terreno/settings.py`).

Changing the systemd unit or nginx config happens **on the server**, not via
this repo. If you change them, update this README to match.

## History

An older manual `deploy.sh` + config templates (`nginx.conf`,
`gunicorn_config.py`, `mariachi-website.service`) lived in this directory;
they referenced a different service name, path, and branch and did not match
the live setup. Removed 2026-07 — see git history if needed.
