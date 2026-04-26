# Server Setup — Complete Guide
## How mariachiesencia.com Went From a Blank Ubuntu Box to a Live Django Site

*Part of the Mariachi Todo Terreno Learning Series — Section 05: DevOps & Infrastructure*

---

## Who This Is For

This document is for anyone on the team who wants to understand **exactly** what was done on the server to get the site running. Every command is here, along with an explanation of *why* it was needed. If the server ever needs to be rebuilt from scratch, this is the playbook.

---

## The Big Picture

Before diving in, here's the architecture we end up with:

```
Internet
   │
   ▼
nginx (port 80/443)          ← handles HTTPS, serves static files
   │
   ├── /django-static/ ──→ /var/www/mariachi-django-static/  (CSS, JS, images)
   │
   └── everything else ──→ Gunicorn (127.0.0.1:8000)         (the Django app)
                                │
                                ▼
                          Django 5.2.8
                                │
                                ▼
                          PostgreSQL                           (the database)
```

**nginx** is the public-facing web server. It speaks HTTPS, handles certificates, and serves your CSS/images directly (fast, no Python needed). For anything that's a real page request, it hands off to **Gunicorn**, which is a production-grade Python web server. Gunicorn runs your Django code and returns HTML. Django talks to **PostgreSQL** to store and retrieve data.

---

## Server Details

| Item | Value |
|------|-------|
| Server | Physical dedicated Ubuntu server (not a VPS) |
| Hostname | `mariachiesencia.com` |
| IP | `72.204.116.227` |
| OS | Ubuntu (22.04 LTS) |
| User | `nekrosys` |
| Project path | `/home/nekrosys/mariachi-django/` |
| Static files | `/var/www/mariachi-django-static/` |
| Python venv | `/home/nekrosys/mariachi-django/venv/` |

---

## Phase 1 — System-Level Packages

These are installed once at the OS level, before any Python code is involved.

### 1.1 Update the Package List

```bash
sudo apt update && sudo apt upgrade -y
```

**Why?** Always start with an updated package list so you get the latest versions of everything.

---

### 1.2 Install Python 3, pip, and venv

```bash
sudo apt install python3 python3-pip python3-venv -y
```

**Why?**
- `python3` — the Python interpreter. Ubuntu doesn't ship with it by default on minimal installs.
- `python3-pip` — the Python package manager.
- `python3-venv` — lets you create isolated virtual environments (see Phase 2).

---

### 1.3 Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

**Why?** Django can use SQLite for development but SQLite is not suitable for production (no concurrent writes, no network access). PostgreSQL is the industry-standard choice for web applications.

After installation, PostgreSQL starts automatically. You can check it with:

```bash
sudo systemctl status postgresql
```

---

### 1.4 Install nginx

```bash
sudo apt install nginx -y
```

**Why?** Gunicorn is excellent at running Python but it's not designed to serve thousands of users directly or handle HTTPS. nginx sits in front and handles all of that.

---

### 1.5 Install Certbot (for HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
```

**Why?** This is the tool that gets free SSL/TLS certificates from Let's Encrypt. Without it, the site would only work over HTTP and browsers would show "Not Secure".

---

### 1.6 Install git

```bash
sudo apt install git -y
```

**Why?** To clone the project repository from GitHub.

---

### 1.7 Install build tools (required for some Python packages)

```bash
sudo apt install build-essential libpq-dev -y
```

**Why?**
- `build-essential` — includes `gcc`, `make`, and other C compilation tools. Some Python packages (like `psycopg2`) include C extensions that must be compiled during `pip install`.
- `libpq-dev` — the PostgreSQL development headers. `psycopg2` (Django's PostgreSQL driver) needs these to compile.

---

## Phase 2 — PostgreSQL Database Setup

### 2.1 Create the Database User

```bash
sudo -u postgres psql
```

Inside the PostgreSQL shell:

```sql
CREATE USER mariachi_user WITH PASSWORD 'MariachiDB2026';
```

**Why?** Never use the default `postgres` superuser for your application. Create a dedicated user with only the permissions it needs (principle of least privilege).

---

### 2.2 Create the Database

```sql
CREATE DATABASE mariachi_db OWNER mariachi_user;
GRANT ALL PRIVILEGES ON DATABASE mariachi_db TO mariachi_user;
\q
```

**Why?** The database needs to exist before Django can connect to it or run migrations.

---

## Phase 3 — Python Virtual Environment & Django

### 3.1 Clone the Repository

```bash
cd /home/nekrosys
git clone git@github.com:g0ochoa/python-mariachi-website.git mariachi-django
cd mariachi-django
```

---

### 3.2 Create the Virtual Environment

```bash
python3 -m venv venv
```

**Why a virtual environment?** If you installed packages globally, every project on the server would share the same packages. Project A might need Django 4.2, Project B might need Django 5.2 — they can't coexist globally. A virtual environment is an isolated folder that contains its own copy of Python and all packages, completely separate from the system and from other projects.

The `venv` folder lives at `/home/nekrosys/mariachi-django/venv/`.

---

### 3.3 Activate the Venv and Install Packages

```bash
source venv/bin/activate
pip install -r requirements.txt
```

Key packages this installs:

| Package | Purpose |
|---------|---------|
| `Django` | The web framework |
| `gunicorn` | Production WSGI server to run Django |
| `psycopg2` | PostgreSQL driver (lets Django talk to Postgres) |
| `python-dotenv` or `django-environ` | Load secrets from `.env` file |
| `whitenoise` | (if used) Serve static files from Python |
| `social-auth-app-django` | Google OAuth login |

---

### 3.4 Create the `.env` File

```bash
nano /home/nekrosys/mariachi-django/.env
```

Contents:

```env
SECRET_KEY=your-long-random-django-secret-key
DEBUG=False
ALLOWED_HOSTS=mariachiesencia.com,www.mariachiesencia.com
DATABASE_URL=postgres://mariachi_user:MariachiDB2026@localhost:5432/mariachi_db
```

**Why?** The `.env` file holds secrets that should never be committed to git. The `.gitignore` excludes it. On the server it's the only place these values live.

---

### 3.5 Run Migrations

```bash
cd /home/nekrosys/mariachi-django
venv/bin/python manage.py migrate
```

**Why?** Migrations create all the database tables. Without this, Django can't store any data — logins, contact forms, etc. would all fail.

---

### 3.6 Collect Static Files

```bash
venv/bin/python manage.py collectstatic --noinput
```

**Why?** Django's development server can serve your CSS/JS directly. In production, it can't (and shouldn't). `collectstatic` gathers every static file from across the project into one directory (`staticfiles/`), from where nginx can serve them efficiently.

---

### 3.7 Create the Superuser

```bash
venv/bin/python manage.py createsuperuser
```

This creates the admin account used to access `/admin/`. Follow the prompts.

---

### 3.8 Seed the Scores Data

```bash
venv/bin/python manage.py loaddata scores_fixture.json
```

This populated the database with 996 songs for the portal library.

---

## Phase 4 — Gunicorn systemd Service

Gunicorn needs to run continuously in the background, start on boot, and restart if it crashes. That's what a **systemd service** does.

### 4.1 Create the Service File

```bash
sudo nano /etc/systemd/system/mariachi-django.service
```

Contents:

```ini
[Unit]
Description=Gunicorn daemon for Mariachi Django
After=network.target

[Service]
User=nekrosys
Group=www-data
WorkingDirectory=/home/nekrosys/mariachi-django
ExecStart=/home/nekrosys/mariachi-django/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          mariachi_todo_terreno.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Explaining each line:**

- `User=nekrosys` — Gunicorn runs as the `nekrosys` user (not root — never run web services as root)
- `Group=www-data` — also belongs to the `www-data` group (nginx's group), so nginx can communicate with it
- `WorkingDirectory` — where to run from (so relative paths in settings work)
- `ExecStart` — the actual command: use the venv's gunicorn, 3 worker processes, bind to localhost port 8000
- `--workers 3` — rule of thumb is `(2 × CPU cores) + 1`. This server has 1 core, so 3 workers
- `--bind 127.0.0.1:8000` — only listen on localhost, not the public internet (nginx is the public face)
- `Restart=on-failure` — automatically restart if Gunicorn crashes

---

### 4.2 Enable and Start the Service

```bash
sudo systemctl daemon-reload        # tell systemd to read the new file
sudo systemctl enable mariachi-django  # start automatically on boot
sudo systemctl start mariachi-django   # start it now
sudo systemctl status mariachi-django  # verify it's running
```

---

## Phase 5 — nginx Configuration

nginx handles:
1. HTTP → HTTPS redirect
2. HTTPS termination (SSL certificates)
3. Serving static files directly (fast)
4. Proxying everything else to Gunicorn

### 5.1 Create the Site Config

```bash
sudo nano /etc/nginx/sites-available/mariachiesencia
```

Contents:

```nginx
server {
    listen 80;
    server_name mariachiesencia.com www.mariachiesencia.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name mariachiesencia.com www.mariachiesencia.com;

    ssl_certificate /etc/letsencrypt/live/mariachiesencia.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mariachiesencia.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    client_max_body_size 20M;

    # Serve static files directly — no Python involved
    location ^~ /django-static/ {
        alias /var/www/mariachi-django-static/;
    }

    # Everything else → Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 5.2 Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/mariachiesencia /etc/nginx/sites-enabled/
sudo nginx -t        # test config syntax
sudo systemctl reload nginx
```

**Why `ln -s`?** nginx has two folders: `sites-available/` (all configs) and `sites-enabled/` (active configs). Creating a symlink is the standard way to "enable" a site without duplicating the file.

---

### 5.3 Get the SSL Certificate

```bash
sudo certbot --nginx -d mariachiesencia.com -d www.mariachiesencia.com
```

Certbot will:
1. Verify ownership of the domain (by creating a temporary file nginx serves)
2. Download the certificate from Let's Encrypt
3. Automatically update the nginx config with the certificate paths
4. Set up a cron job to auto-renew before expiry

---

## Phase 6 — Static Files: The Permission Problem

This was the trickiest issue. Here's the full story.

### The Problem

After deploying, the live site had **no CSS** — everything was unstyled. Checking the browser dev tools showed:

```
GET https://mariachiesencia.com/django-static/css/style.css  → 403 Forbidden
```

nginx could **find** the file but couldn't **read** it.

### Why It Happened

`collectstatic` puts files in `/home/nekrosys/mariachi-django/staticfiles/`. The original nginx config pointed there:

```nginx
location ^~ /django-static/ {
    alias /home/nekrosys/mariachi-django/staticfiles/;
}
```

The file permissions on `style.css` looked fine:
```
-rw-r--r-- 1 nekrosys nekrosys  style.css
```

But the **home directory** itself had `drwxr-x---` permissions:

```
drwxr-x---  nekrosys nekrosys  /home/nekrosys/
```

The last group of `---` means "others" (everyone who isn't `nekrosys` or in the `nekrosys` group) get **no access at all** — not even the ability to traverse (enter) the directory.

nginx runs as `www-data`, which is "other" here. So even though the CSS file was readable, nginx couldn't reach it because it couldn't enter `/home/nekrosys/` to begin with. This is like a locked front door — it doesn't matter if the room inside is unlocked.

### The Fix

Move static files somewhere nginx can access without needing to enter the home directory:

```bash
# Create a world-accessible location for static files
sudo mkdir -p /var/www/mariachi-django-static

# Copy the collected static files there
sudo cp -r /home/nekrosys/mariachi-django/staticfiles/* /var/www/mariachi-django-static/

# Give nginx (www-data) ownership
sudo chown -R www-data:www-data /var/www/mariachi-django-static

# Ensure directories are traversable and files are readable
sudo chmod -R 755 /var/www/mariachi-django-static
```

Then update the nginx config:

```nginx
# Before (broken):
alias /home/nekrosys/mariachi-django/staticfiles/;

# After (working):
alias /var/www/mariachi-django-static/;
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

Verify the fix:
```bash
curl -sI https://mariachiesencia.com/django-static/css/style.css | head -3
# Should return: HTTP/2 200
```

---

## Phase 7 — Passwordless sudo for the Deploy Pipeline

The GitHub Actions pipeline SSHs into the server and runs commands. One of those commands is `sudo systemctl restart mariachi-django`. By default, `sudo` requires a password — but the pipeline has no way to type a password interactively.

### The Solution: a Targeted sudoers Rule

Instead of giving `nekrosys` full passwordless sudo (a major security risk), we created a rule that grants passwordless `sudo` for **only the specific commands the pipeline needs**:

```bash
sudo visudo -f /etc/sudoers.d/mariachi-django
```

Contents:

```
nekrosys ALL=(ALL) NOPASSWD: /bin/systemctl restart mariachi-django, /bin/cp -r * /var/www/mariachi-django-static/, /bin/chown -R www-data:www-data /var/www/mariachi-django-static/
```

**Why this approach is safe:**
- The rule is in its own file (`/etc/sudoers.d/mariachi-django`) — easy to audit and remove
- Only three specific commands are allowed without a password
- All other `sudo` commands still require the password
- The pipeline can restart the app and copy static files, nothing else

---

## Phase 8 — SSH Key Authentication for the Pipeline

GitHub Actions needs to SSH into the server. Password-based SSH in a CI/CD pipeline is insecure and impractical. The solution is an SSH key pair.

### 8.1 Generate a Key Pair (on your local machine)

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions-deploy" -f ~/.ssh/mariachi_deploy_key
```

This creates two files:
- `~/.ssh/mariachi_deploy_key` — **private key** (goes into GitHub Secrets)
- `~/.ssh/mariachi_deploy_key.pub` — **public key** (goes onto the server)

### 8.2 Add the Public Key to the Server

```bash
ssh-copy-id -i ~/.ssh/mariachi_deploy_key.pub nekrosys@mariachiesencia.com
```

This appends the public key to `/home/nekrosys/.ssh/authorized_keys`.

### 8.3 Add the Private Key to GitHub

1. Go to the GitHub repo → **Settings** → **Secrets and variables** → **Actions** → **Secrets**
2. Create a secret named `STAGING_SSH_KEY`
3. Paste the contents of `~/.ssh/mariachi_deploy_key` (the private key)

The pipeline uses the [webfactory/ssh-agent](https://github.com/webfactory/ssh-agent) action to load this key into an SSH agent, then uses it for rsync and SSH commands.

---

## Quick Reference — Useful Server Commands

```bash
# Check if Gunicorn is running
sudo systemctl status mariachi-django

# Restart Gunicorn (after a code change)
sudo systemctl restart mariachi-django

# View Gunicorn logs (last 50 lines)
sudo journalctl -u mariachi-django -n 50 --no-pager

# Check nginx config syntax
sudo nginx -t

# Reload nginx (after config change, no downtime)
sudo systemctl reload nginx

# Restart nginx completely
sudo systemctl restart nginx

# View nginx error log
sudo tail -f /var/log/nginx/error.log

# View nginx access log
sudo tail -f /var/log/nginx/access.log

# Check PostgreSQL status
sudo systemctl status postgresql

# Connect to the database
sudo -u postgres psql mariachi_db

# Run Django management commands manually
cd /home/nekrosys/mariachi-django
venv/bin/python manage.py [command]

# Check SSL certificate expiry
sudo certbot certificates

# Manually renew SSL certificates
sudo certbot renew --dry-run
```

---

## Directory Map

```
/
├── etc/
│   ├── nginx/
│   │   ├── nginx.conf                      ← main nginx config
│   │   ├── sites-available/
│   │   │   └── mariachiesencia             ← our site config
│   │   └── sites-enabled/
│   │       └── mariachiesencia → ../sites-available/mariachiesencia  (symlink)
│   ├── systemd/system/
│   │   └── mariachi-django.service         ← Gunicorn service definition
│   ├── sudoers.d/
│   │   └── mariachi-django                 ← passwordless sudo rules
│   └── letsencrypt/
│       └── live/mariachiesencia.com/       ← SSL certificates
│           ├── fullchain.pem
│           └── privkey.pem
│
├── var/
│   └── www/
│       └── mariachi-django-static/         ← static files served by nginx
│           ├── css/
│           │   └── style.css
│           ├── js/
│           └── admin/
│
└── home/
    └── nekrosys/
        └── mariachi-django/                ← the Django project
            ├── .env                        ← secrets (never committed to git)
            ├── manage.py
            ├── requirements.txt
            ├── staticfiles/                ← collectstatic output (source, not served)
            ├── venv/                       ← Python virtual environment
            └── mariachi_todo_terreno/      ← Django project package
                └── settings.py
```

---

## Self-Check Questions

Test your understanding:

1. **Why does nginx sit in front of Gunicorn instead of Gunicorn serving requests directly?**
2. **Why was the CSS returning 403 even though the file had `rw-r--r--` permissions?**
3. **What is the difference between `sites-available` and `sites-enabled` in nginx?**
4. **Why do we use `--bind 127.0.0.1:8000` instead of `--bind 0.0.0.0:8000` for Gunicorn?**
5. **Why is `/var/www/mariachi-django-static/` better than serving static files from `/home/nekrosys/` for nginx?**
6. **What is the risk of giving `nekrosys` full passwordless sudo, and how did we avoid it?**
7. **Why do we use a virtual environment instead of installing packages system-wide?**
8. **What does `systemctl enable` do differently from `systemctl start`?**

<details>
<summary>Answers</summary>

1. nginx handles HTTPS, compression, rate limiting, and serves static files extremely fast without involving Python. It also provides a layer of protection — Gunicorn never faces the public internet directly.

2. The file's own permissions were fine, but nginx couldn't *traverse* into `/home/nekrosys/` because that directory had `drwxr-x---` — no access for "others". Directory traversal requires execute permission (`x`) on every directory in the path.

3. `sites-available` stores all config files. `sites-enabled` contains symlinks to the ones nginx should actually load. This lets you prepare configs without activating them.

4. `127.0.0.1` means only local connections (from nginx on the same machine) can reach Gunicorn. `0.0.0.0` would expose it to the whole internet on port 8000, bypassing nginx and all its protections.

5. `/var/www/` is world-accessible by default (`drwxr-xr-x`). `/home/nekrosys/` has restricted permissions by design — home directories are private. nginx runs as `www-data` (an "other" user) so it can't traverse into the home directory.

6. Full passwordless sudo means if someone compromises the pipeline or SSH key, they have root. We limited it to only three specific commands, so even in a worst case, the attacker can only restart Gunicorn and copy static files.

7. System-wide installs would pollute the system Python and create version conflicts between projects. Virtual environments are isolated and portable — you know exactly what's installed and can reproduce it anywhere with `pip install -r requirements.txt`.

8. `systemctl start` starts the service now. `systemctl enable` makes it start automatically every time the server boots. You need both.

</details>
