# Gunicorn configuration file for Mariachi Todo Terreno Django app

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '/var/log/mariachi-website/gunicorn-access.log'
errorlog = '/var/log/mariachi-website/gunicorn-error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'mariachi_todo_terreno'

# Server mechanics
daemon = False
pidfile = '/var/run/mariachi-website/gunicorn.pid'
user = None  # Will be set by systemd
group = None  # Will be set by systemd
umask = 0o077
tmp_upload_dir = None
