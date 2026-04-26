# Chapter 5.1 — CI/CD Pipelines with GitHub Actions
*How we automated deployments for Mariachi Todo Terreno*

---

## What You'll Learn

By the end of this chapter you'll understand:

- What CI/CD is and why every real project uses it
- What a VPS is and how our server is set up
- How GitHub Actions works (the YAML workflow file, step by step)
- How SSH authentication works between GitHub and our server
- How to store secrets safely in GitHub
- How to grant limited passwordless sudo access on a Linux server
- The full deployment flow: from your laptop → GitHub → VPS

---

## Part 1 — The Problem We Were Solving

Before CI/CD, our deployment process looked like this:

```
1. Edit code on laptop
2. Open terminal
3. Type a long rsync command
4. SSH into server
5. Run collectstatic manually
6. Restart Gunicorn manually
7. Hope you didn't forget a step
```

This is called **manual deployment**. It works, but it has real problems:

- **Easy to forget steps** — skip `collectstatic` and your CSS doesn't update
- **Not reproducible** — different people might deploy differently
- **No audit trail** — who deployed what, and when?
- **Risky on a bad day** — tired at 11pm, you might push broken code

**CI/CD solves all of this** by automating the process every time you push to GitHub.

---

## Part 2 — Key Vocabulary

### VPS (Virtual Private Server) vs Dedicated Server
In the industry, "VPS" is often used loosely to mean any remote Linux server you SSH into. Technically:

- **VPS** — a virtualized slice of a shared physical machine (like renting a room in an apartment building)
- **Dedicated Server** — a physical machine all to yourself (like owning the whole building)

Our server at `mariachiesencia.com` is actually a **dedicated physical Ubuntu server** — even better than a VPS. More resources, no noisy neighbors, consistent performance. The CI/CD pipeline works identically for both — it just cares that there's a Linux machine it can SSH into.

Our server:
- **Host**: `mariachiesencia.com` (IP: 72.204.116.227)
- **OS**: Ubuntu Linux
- **Type**: Physical dedicated server
- **User**: `nekrosys`

### CI/CD
**CI = Continuous Integration** — automatically test and validate code whenever someone pushes  
**CD = Continuous Deployment** — automatically deploy to a server after the code passes

Together: every `git push` to `main` automatically runs a tested, repeatable deployment. No humans required.

### GitHub Actions
GitHub's built-in CI/CD system. You define a **workflow** in a YAML file inside your repo. GitHub runs that workflow on its own cloud servers (called **runners**) whenever a trigger fires (like a push to `main`).

### Runner
A temporary cloud computer that GitHub spins up to run your workflow. It's a fresh Ubuntu machine every time. It checks out your code, runs your steps, then disappears.

### Workflow
The YAML file that defines what to do. Lives at `.github/workflows/your-workflow.yml`.

---

## Part 3 — Our Workflow File Explained

Here is our complete workflow file at `.github/workflows/deploy-staging.yml`, broken down section by section:

```yaml
name: Deploy to Staging
```
The display name shown in the GitHub Actions UI.

```yaml
on:
  push:
    branches:
      - main
```
**The trigger.** This workflow fires whenever code is pushed to the `main` branch. Push to `dev`? Nothing happens. Merge `dev` into `main`? Deploy fires.

```yaml
jobs:
  deploy:
    name: Deploy to VPS Staging
    runs-on: ubuntu-latest
```
A **job** is a group of steps that run together on one runner. `runs-on: ubuntu-latest` means GitHub spins up a fresh Ubuntu machine for us.

---

### Step 1 — Checkout code

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```
`uses` means we're using a **pre-built Action** from GitHub's marketplace. `actions/checkout` is the official action that clones your repository onto the runner. Without this, the runner has no code to work with.

---

### Step 2 — Configure SSH

```yaml
- name: Configure SSH
  uses: webfactory/ssh-agent@v0.9.0
  with:
    ssh-private-key: ${{ secrets.STAGING_SSH_KEY }}
```
This loads our SSH private key into the runner's SSH agent so it can authenticate to our VPS. `${{ secrets.STAGING_SSH_KEY }}` reads the secret we stored in GitHub — the runner never prints it to logs.

**Why SSH keys instead of a password?**  
Passwords over automated scripts are dangerous — you'd have to store them in plain text somewhere. SSH key pairs are cryptographically secure. The private key stays secret; the public key sits on the server in `~/.ssh/authorized_keys`.

---

### Step 3 — Add server to known_hosts

```yaml
- name: Add server to known_hosts
  run: |
    ssh-keyscan -H ${{ vars.STAGING_HOST }} >> ~/.ssh/known_hosts
```
The first time SSH connects to any server, it asks: *"Do you trust this server?"* In an automated pipeline there's nobody to type "yes". `ssh-keyscan` fetches the server's fingerprint and adds it to `known_hosts` so SSH stops asking.

`${{ vars.STAGING_HOST }}` reads from **Variables** (not Secrets) — it's just `mariachiesencia.com`, not sensitive.

---

### Step 4 — Sync files to server

```yaml
- name: Sync files to server
  run: |
    rsync -avz --delete \
      --exclude='.git/' \
      --exclude='.env' \
      --exclude='venv/' \
      ...
      ./ ${{ vars.STAGING_USER }}@${{ vars.STAGING_HOST }}:${{ vars.STAGING_PROJECT_PATH }}/
```
`rsync` is a tool that efficiently syncs files between two locations. It only transfers files that changed — not the whole project every time.

Flag breakdown:
- `-a` — archive mode (preserves permissions, timestamps, symlinks)
- `-v` — verbose (prints what it's doing)
- `-z` — compress data during transfer
- `--delete` — remove files on the server that no longer exist locally
- `--exclude` — skip these paths (never send `.env` passwords or the `venv/` virtualenv)

---

### Step 5 — Run post-deploy commands

```yaml
- name: Run post-deploy commands
  run: |
    ssh nekrosys@mariachiesencia.com << 'EOF'
      set -e
      cd /home/nekrosys/mariachi-django

      venv/bin/pip install -q -r requirements.txt
      venv/bin/python manage.py migrate --noinput
      venv/bin/python manage.py collectstatic --noinput --clear
      sudo systemctl restart mariachi-django
    EOF
```

This SSHes into the server and runs commands remotely. The `<< 'EOF'` syntax is a **heredoc** — everything between `EOF` markers is sent as a script to the remote server.

What each command does:

| Command | Purpose |
|---|---|
| `set -e` | Stop immediately if any command fails (don't silently continue) |
| `venv/bin/pip install -r requirements.txt` | Install any new Python packages |
| `manage.py migrate --noinput` | Apply any pending database migrations |
| `manage.py collectstatic --noinput --clear` | Copy all static files (CSS, JS, images) into `staticfiles/` so nginx can serve them |
| `sudo systemctl restart mariachi-django` | Restart Gunicorn so it picks up the new code |

**Why `venv/bin/pip` instead of just `pip`?**  
The runner's SSH session doesn't activate the virtualenv automatically. Using the full path `venv/bin/pip` and `venv/bin/python` ensures we're using the project's isolated Python, not the system Python.

---

## Part 4 — Secrets vs Variables

GitHub gives you two places to store configuration:

| | **Secrets** | **Variables** |
|---|---|---|
| **Use for** | Passwords, private keys, tokens | Hostnames, usernames, paths |
| **Visible in logs?** | Never — masked as `***` | Yes |
| **Syntax** | `${{ secrets.NAME }}` | `${{ vars.NAME }}` |

Our split:

```
Secrets:
  STAGING_SSH_KEY  → the private key (-----BEGIN OPENSSH PRIVATE KEY-----)

Variables:
  STAGING_HOST          → mariachiesencia.com
  STAGING_USER          → nekrosys
  STAGING_PROJECT_PATH  → /home/nekrosys/mariachi-django
```

The rule of thumb: if someone seeing it could cause damage, it's a Secret. A hostname is public information — it's literally in your browser's address bar.

---

## Part 5 — The Sudo Problem and How We Fixed It

### The problem

Our post-deploy script needed to run:
```bash
sudo systemctl restart mariachi-django
```

But `sudo` normally asks for a password. The GitHub Actions runner can't type a password — there's no human there and no terminal (no TTY).

First error we saw:
```
sudo: a terminal is required to read the password; either use the -S option
sudo: a password is required
```

### Why not just use `-S` to pipe the password?

We could do `echo 'password' | sudo -S systemctl restart`, but that means storing the server password as a GitHub Secret. That works, but it's not best practice — if someone ever gets that secret, they have the full sudo password for the entire server.

### The right solution: targeted passwordless sudo

We gave `nekrosys` permission to run **only that one specific command** without a password:

```bash
# On the server, we ran:
echo 'nekrosys ALL=(ALL) NOPASSWD: /bin/systemctl restart mariachi-django' \
  > /etc/sudoers.d/mariachi-django
chmod 440 /etc/sudoers.d/mariachi-django
```

This creates a file in `/etc/sudoers.d/` (the proper place to add sudo rules without editing the main sudoers file). It says:

> "User `nekrosys` can run `/bin/systemctl restart mariachi-django` as any user, without a password."

Nothing else. Not `systemctl stop`, not `rm -rf`, just that one command. This is the **principle of least privilege** — grant only the minimum access needed.

We validated the syntax with `visudo -c` before applying, which checks for errors before saving (a bad sudoers file can lock you out of sudo entirely).

---

## Part 6 — The Full Picture

Here's the complete flow from your laptop to the live website:

```
Your Laptop
    │
    │  git push origin main
    ▼
GitHub.com
    │  Trigger: push to main detected
    │  GitHub spins up a fresh Ubuntu runner
    ▼
GitHub Actions Runner (temporary cloud machine)
    │
    ├─ 1. Clone the repo
    ├─ 2. Load SSH private key into ssh-agent
    ├─ 3. Add VPS fingerprint to known_hosts
    ├─ 4. rsync changed files → VPS
    └─ 5. SSH into VPS and run:
           pip install
           migrate
           collectstatic
           sudo systemctl restart mariachi-django
    │
    ▼
VPS (mariachiesencia.com)
    │
    ├─ /home/nekrosys/mariachi-django/   ← updated code
    ├─ /home/nekrosys/mariachi-django/staticfiles/  ← new CSS/JS
    └─ mariachi-django.service (Gunicorn)  ← restarted, serving new code
    │
    ▼
nginx (always running)
    │  Receives visitor's HTTP request
    ├─ /django-static/ → staticfiles/ (CSS, JS, images)
    └─ everything else → Gunicorn → Django app
    │
    ▼
Visitor's Browser at mariachiesencia.com
```

---

## Part 7 — Why This Matters

Before this session, deploying the mariachi site meant:
- Opening a terminal
- Remembering the rsync command
- SSH-ing into the server
- Running 3 more commands manually
- Hoping nothing went wrong

Now deploying means:
```bash
git push origin main
```

That's it. 17 seconds later the site is updated. Every team member can deploy. Every deployment is identical. There's a full audit log in GitHub of who deployed what and when.

This is the foundation of professional software delivery. Every company — from startups to Netflix — operates some version of this pipeline.

---

## Self-Check Questions

Test your understanding:

1. What does VPS stand for, and how is it different from shared hosting?
2. What is a GitHub Actions **runner** and how long does it exist?
3. Why do we exclude `.env` from the rsync transfer?
4. What does `collectstatic` do and why must it run after every deploy?
5. Why is `set -e` at the top of the post-deploy script important?
6. What is the difference between a GitHub Secret and a GitHub Variable?
7. Why is a targeted sudoers rule safer than storing the full sudo password as a secret?
8. What would happen if we forgot to add the server to `known_hosts`?

---

## Key Commands Reference

```bash
# Trigger a deploy (just push to main)
git push origin main

# Check the deploy log on the server
ssh nekrosys@mariachiesencia.com "journalctl -u mariachi-django -n 30 --no-pager"

# Check if Gunicorn is running
ssh nekrosys@mariachiesencia.com "systemctl is-active mariachi-django"

# Manually collect static files on server
ssh nekrosys@mariachiesencia.com "cd /home/nekrosys/mariachi-django && venv/bin/python manage.py collectstatic --noinput --clear"

# View the sudoers rule we created
ssh nekrosys@mariachiesencia.com "cat /etc/sudoers.d/mariachi-django"
```
