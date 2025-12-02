# Django Project Setup Guide
**Mariachi Todo Terreno Website - Complete Django Installation & Configuration**

*Author: Gerry Ochoa*  
*Date: December 1, 2025*  
*Sprint: Sprint 2, Day 1*  
*Platform: Windows PC (PowerShell)*

---

## 📚 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Project Structure Overview](#project-structure-overview)
3. [Step-by-Step Setup Guide](#step-by-step-setup-guide)
4. [Understanding Django Components](#understanding-django-components)
5. [Team Setup Instructions](#team-setup-instructions)
6. [Common Issues & Solutions](#common-issues--solutions)
7. [Next Steps](#next-steps)

---

## 📋 **Prerequisites**

Before starting, ensure you have:
- Python 3.11+ installed
- Virtual environment created and activated
- Git repository cloned
- Terminal/PowerShell access

**Check your Python version:**
```powershell
python --version
# Should show: Python 3.11.x or higher
```

---

## 🏗️ **Project Structure Overview**

### **Final Directory Structure**
```
python-mariachi-website/
├── manage.py                      # Django management tool
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (secrets) - NOT in Git
├── .env.example                  # Template for .env - IN Git
├── db.sqlite3                    # SQLite database - NOT in Git
├── mariachi_todo_terreno/        # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # URL routing
│   ├── asgi.py                   # ASGI config (for async)
│   └── wsgi.py                   # WSGI config (for deployment)
├── accounts/                     # Authentication app
│   ├── migrations/               # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Admin interface config
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models (User)
│   ├── views.py                  # View logic
│   └── tests.py                  # Unit tests
├── public_site/                  # Public-facing app
│   └── (same structure as accounts)
└── musicians_portal/             # Private portal app
    └── (same structure as accounts)
```

### **What Each Component Does**

**`manage.py`**  
- Command-line utility for Django operations
- Run migrations, start server, create users, etc.
- Never edit this file

**Project Folder (`mariachi_todo_terreno/`)**  
- Contains project-wide settings and configuration
- NOT an app - it's the configuration hub
- All apps connect through this

**Apps (`accounts/`, `public_site/`, `musicians_portal/`)**  
- Self-contained modules for specific features
- Each has own models, views, URLs
- Apps are siblings to project folder, NOT inside it

---

## 🚀 **Step-by-Step Setup Guide**

### **Step 1: Install Django and Dependencies**

**Command:**
```powershell
pip install django psycopg2-binary python-dotenv django-htmx
```

**What Each Package Does:**

| Package | Purpose | Why We Need It |
|---------|---------|----------------|
| `django` | Web framework | Core framework for building the website |
| `psycopg2-binary` | PostgreSQL adapter | Allows Django to communicate with PostgreSQL database |
| `python-dotenv` | Environment variables | Loads secrets from .env file (keeps passwords out of code) |
| `django-htmx` | HTMX integration | Enables dynamic page updates without full page reloads |

**Expected Output:**
```
Successfully installed django-5.2.8 psycopg2-binary-2.9.11 python-dotenv-1.2.1 django-htmx-1.27.0
```

---

### **Step 2: Create Django Project**

**Command:**
```powershell
django-admin startproject mariachi_todo_terreno .
```

**Breaking Down the Command:**
- `django-admin` = Django's administrative command-line tool
- `startproject` = Creates a new Django project
- `mariachi_todo_terreno` = Your project name (use underscores, not hyphens)
- `.` = Create in current directory (don't create extra subfolder)

**What Gets Created:**
```
mariachi_todo_terreno/
├── __init__.py          # Makes Python treat this as a package
├── settings.py          # All project settings (database, apps, middleware)
├── urls.py              # URL routing (maps URLs to views)
├── asgi.py              # Async Server Gateway Interface config
└── wsgi.py              # Web Server Gateway Interface config

manage.py                # Your main Django command tool
```

**Why This Matters:**
- `settings.py` is where you configure everything (database, installed apps, security)
- `urls.py` is your website's navigation map
- `manage.py` is how you interact with Django (run server, migrations, etc.)

---

### **Step 3: Create Django Apps**

**Commands:**
```powershell
python manage.py startapp public_site
python manage.py startapp musicians_portal
python manage.py startapp accounts
```

**Understanding `startapp`:**
- Creates a self-contained module for specific functionality
- Each app has models (database), views (logic), admin (interface)
- Apps can be reused in other Django projects

**What Each App Does:**

**`accounts`** - Authentication & User Management
- Customer registration (for promos/bookings)
- Musician login (Google SSO)
- Role-based permissions (customer/musician/admin)
- Custom User model with extended fields

**`public_site`** - Public-Facing Website
- Home page with hero section
- About the mariachi group
- Photo/video gallery
- Contact form and booking requests
- Customer registration forms

**`musicians_portal`** - Private Band Member Portal
- Score library (994+ songs with search/filter)
- Practice tools (metronome, audio recorder)
- Event calendar
- File sharing for recordings
- Only accessible to musicians and admins

**Key Concept - Apps vs. Project:**
```
❌ WRONG:
mariachi_todo_terreno/
└── accounts/          # DON'T put apps inside project folder

✅ CORRECT:
python-mariachi-website/
├── mariachi_todo_terreno/    # Project config (sibling)
├── accounts/                  # App (sibling)
├── public_site/               # App (sibling)
└── musicians_portal/          # App (sibling)
```

---

### **Step 4: Configure Django Settings**

**File to Edit:** `mariachi_todo_terreno/settings.py`

**Add Environment Variables (Top of File):**
```python
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
```

**Why:** Keeps secrets (passwords, API keys) out of code

**Register Your Apps:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',         # Django admin interface
    'django.contrib.auth',          # Authentication system
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',      # Session framework
    'django.contrib.messages',      # Messaging framework
    'django.contrib.staticfiles',   # Static file management
    # Third-party apps
    'django_htmx',                  # HTMX integration
    # Local apps
    'accounts',                     # Your authentication app
    'public_site',                  # Your public website app
    'musicians_portal',             # Your private portal app
]
```

**Why This Order Matters:**
1. Django built-in apps first (always)
2. Third-party apps next (like django_htmx)
3. Your local apps last

**Use Environment Variables for Secrets:**
```python
# Before (INSECURE - secret exposed in code):
SECRET_KEY = 'django-insecure-u@c!plx5_x3uya...'

# After (SECURE - secret in .env file):
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-for-testing')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

**Tell Django About Custom User Model:**
```python
# At bottom of settings.py
AUTH_USER_MODEL = 'accounts.User'
```

**⚠️ CRITICAL:** Must do this BEFORE first migration. Can't easily change later.

---

### **Step 5: Create Custom User Model**

**File to Edit:** `accounts/models.py`

**Complete User Model Code:**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model supporting customers and musicians.
    Extends Django's built-in User with additional fields.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('musician', 'Musician'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        default='customer',
        help_text='User role determines access permissions'
    )
    
    # Customer-specific fields
    phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Contact phone number'
    )
    promo_opt_in = models.BooleanField(
        default=False,
        help_text='Opted in to receive promotional emails'
    )
    
    # Musician-specific fields (nullable for customers)
    instrument = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text='Primary instrument for musicians'
    )
    google_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        unique=True,
        help_text='Google Workspace ID for SSO authentication'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['username']
```

**Understanding the Model:**

**`AbstractUser`**  
- Django's built-in User class (includes username, password, email, etc.)
- We extend it instead of replacing it
- Keeps Django's authentication system working

**Field Types Explained:**

| Field Type | What It Does | Example |
|------------|--------------|---------|
| `CharField` | Text (limited length) | Username, phone, instrument |
| `BooleanField` | True/False | promo_opt_in |
| `choices=` | Dropdown options | customer/musician/admin |
| `blank=True` | Optional in forms | Phone not required |
| `null=True` | Optional in database | Instrument can be NULL |
| `unique=True` | No duplicates allowed | Only one user per google_id |
| `default=` | Value if not provided | Role defaults to 'customer' |

**Three User Types:**
1. **Customer** - Public user (registers for promos, makes bookings)
2. **Musician** - Band member (access to portal, scores, practice tools)
3. **Admin** - Full access (Gerry - can manage everything)

---

### **Step 6: Create Database Migrations**

**Command:**
```powershell
python manage.py makemigrations
```

**What This Does:**
- Scans all models in your apps
- Detects changes from last migration
- Creates Python file with database change instructions
- Does NOT modify database yet

**Expected Output:**
```
Migrations for 'accounts':
  accounts\migrations\0001_initial.py
    - Create model User
```

**What Gets Created:**
- `accounts/migrations/0001_initial.py` - Migration file with SQL instructions
- Contains code to create User table with all fields

**Understanding Migrations:**
- Django's way of version controlling your database
- Like Git commits, but for database schema
- Allows team to sync database structure
- Can roll back changes if needed

---

### **Step 7: Apply Migrations to Database**

**Command:**
```powershell
python manage.py migrate
```

**What This Does:**
- Reads all migration files (yours + Django's built-in)
- Executes SQL to create/modify database tables
- Creates `db.sqlite3` file (SQLite database)
- Tracks which migrations have been applied

**Expected Output:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
```

**What Tables Get Created:**

| Table | Purpose | Created By |
|-------|---------|------------|
| `accounts_user` | Your custom User table | Your accounts app |
| `django_admin_log` | Admin action history | Django admin app |
| `auth_permission` | Permissions system | Django auth app |
| `auth_group` | User groups | Django auth app |
| `django_session` | User sessions (login) | Django sessions app |
| `django_content_type` | App/model tracking | Django contenttypes |

**Verify Database Was Created:**
```powershell
ls *.sqlite3
# Should show: db.sqlite3 (135 KB or similar)
```

---

### **Step 8: Create Superuser (Admin Account)**

**Command:**
```powershell
python manage.py createsuperuser
```

**What You'll Be Asked:**
```
Username: gerry
Email address: gerryochoatorres@gmail.com
Password: [your password - won't be visible]
Password (again): [repeat password]
```

**What This Does:**
- Creates a User record in database
- Sets `is_staff = True` (can access admin)
- Sets `is_superuser = True` (has all permissions)
- Hashes password securely (never stores plain text)
- Role defaults to 'customer' (need to change to 'admin' in admin interface)

**Important Note:**
After creating superuser, login to admin and change their role to 'admin' for consistency.

---

### **Step 9: Register User Model in Django Admin**

**File to Edit:** `accounts/admin.py`

**Complete Admin Configuration:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for User model.
    Extends Django's UserAdmin with our custom fields.
    """
    # What columns show in user list
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Filters in right sidebar
    list_filter = ('role', 'is_staff', 'is_active', 'promo_opt_in')
    
    # Search bar functionality
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    # Organize edit form into sections
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Permissions', {
            'fields': ('role',)
        }),
        ('Customer Information', {
            'fields': ('phone', 'promo_opt_in'),
            'description': 'Fields for customer accounts'
        }),
        ('Musician Information', {
            'fields': ('instrument', 'google_id'),
            'description': 'Fields for musician accounts (band members)'
        }),
    )
```

**What `@admin.register(User)` Does:**
- Makes User model visible in Django admin sidebar
- Connects User model to CustomUserAdmin configuration
- Without this, model exists but is invisible in admin

**Admin Features You Get:**
- ✅ List all users with username, email, role
- ✅ Filter by role, staff status, promo opt-in
- ✅ Search by username, email, name, phone
- ✅ Edit users with organized form sections
- ✅ Add new users with role selection

---

### **Step 10: Test Django Development Server**

**Command:**
```powershell
python manage.py runserver
```

**What This Does:**
- Starts Django's built-in development web server
- Runs on `http://127.0.0.1:8000/` (localhost port 8000)
- Auto-reloads when you change code
- NOT for production use (development only)

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 01, 2025 - 19:40:23
Django version 5.2.8, using settings 'mariachi_todo_terreno.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Visit These URLs:**

**`http://localhost:8000/`**  
- Django welcome page (rocket ship)
- Confirms Django is working
- Will be replaced with your home page later

**`http://localhost:8000/admin`**  
- Django admin interface
- Login with superuser credentials (gerry / your password)
- Click "Users" to see and manage users
- Click "Add User" to create new users

**Stop the Server:**
- Press `Ctrl+C` in terminal

---

### **Step 11: Create Requirements File**

**Command:**
```powershell
pip freeze > requirements.txt
```

**What This Does:**
- Lists all installed Python packages and versions
- Creates text file with exact dependencies
- Team can install same versions with `pip install -r requirements.txt`
- Ensures everyone has identical environment

**Generated File Content:**
```
asgiref==3.11.0
Django==5.2.8
django-htmx==1.27.0
psycopg2-binary==2.9.11
python-dotenv==1.2.1
sqlparse==0.5.4
tzdata==2025.2
```

---

### **Step 12: Create Environment Variable Files**

**Create `.env.example` (Template - IN Git):**
```env
# Django Environment Variables Template
# Copy this to .env and fill in actual values

SECRET_KEY=your-secret-key-here
DEBUG=True

# Database (PostgreSQL - future)
# DB_NAME=mariachi_db
# DB_USER=postgres
# DB_PASSWORD=your-password
```

**Create `.env` (Actual Secrets - NOT in Git):**
```env
SECRET_KEY=django-insecure-u@c!plx5_x3uya-cmt9ko%s*iyz8#q6p74k2$1!gwzdjbpzlkf
DEBUG=True
```

**Why Two Files?**
- `.env.example` = Template committed to Git (no secrets)
- `.env` = Actual secrets ignored by Git (never commit)
- Team copies .env.example to .env and fills in their values

**Verify .env is Ignored:**
```powershell
# Check .gitignore contains .env
Select-String -Pattern "^\.env$" .gitignore
```

---

### **Step 13: Commit to Git**

**Stage Files:**
```powershell
git add .
```

**Commit with Detailed Message:**
```powershell
git commit -m "Initialize Django project with custom User model and 3 apps

- Created Django project: mariachi_todo_terreno
- Created 3 apps: accounts, public_site, musicians_portal
- Implemented custom User model with role-based access
- Configured Django admin with User management
- Added environment variable support
- Created requirements.txt for team setup

Sprint 2 Day 1 complete"
```

**Push to GitHub:**
```powershell
git push origin dev
```

**What Gets Committed:**
- ✅ Django project files
- ✅ All 3 apps
- ✅ Migration files
- ✅ requirements.txt
- ✅ .env.example
- ✅ .gitignore

**What Doesn't Get Committed:**
- ❌ .env (secrets)
- ❌ db.sqlite3 (database)
- ❌ mariachi-env/ (virtual environment)
- ❌ __pycache__/ (Python cache)

---

## 🧩 **Understanding Django Components**

### **Django Architecture (MVT Pattern)**

Django uses **Model-View-Template** (MVT):

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Model   │◄────►│   View   │◄────►│ Template │
│(Database)│      │ (Logic)  │      │  (HTML)  │
└──────────┘      └──────────┘      └──────────┘
     │                  │                  │
     │                  │                  │
  models.py         views.py         templates/
```

**Model** - Database structure (what data you store)  
**View** - Business logic (what happens when user visits a page)  
**Template** - HTML presentation (what user sees)

### **Django Request/Response Flow**

```
1. User visits URL: http://localhost:8000/musicians/scores/

2. urls.py routes to view:
   path('musicians/scores/', views.score_library)

3. View queries database:
   scores = Score.objects.filter(user=request.user)

4. View renders template:
   return render(request, 'scores.html', {'scores': scores})

5. Template generates HTML:
   {% for score in scores %}
     <div>{{ score.title }}</div>
   {% endfor %}

6. Browser displays page
```

### **Migration Workflow**

```
1. Change model in models.py
   └─► Add field: role = models.CharField(...)

2. Create migration
   └─► python manage.py makemigrations
       Creates: 0002_user_role.py

3. Review migration (optional)
   └─► Read 0002_user_role.py to see SQL

4. Apply migration
   └─► python manage.py migrate
       Executes: ALTER TABLE accounts_user ADD role VARCHAR(20)

5. Database updated
   └─► Table now has new 'role' column
```

### **App Structure Explained**

Each Django app follows this pattern:

```
accounts/
├── migrations/           # Database version history
│   ├── 0001_initial.py  # First migration (create tables)
│   └── __init__.py
├── __init__.py          # Makes this a Python package
├── admin.py             # Register models in admin interface
├── apps.py              # App configuration
├── models.py            # Database structure (tables, fields)
├── views.py             # Request handling logic
├── tests.py             # Unit tests
└── urls.py              # URL routing (create this file)
```

**When to Create New App:**
- Feature is self-contained and reusable
- Has its own models/database tables
- Can be developed independently
- Example: blog app, payment app, notification app

**When to Add to Existing App:**
- Feature extends existing functionality
- Shares models with existing app
- Tightly coupled to app's purpose
- Example: add password reset to accounts app

---

## 👥 **Team Setup Instructions**

### **For Team Members Cloning the Repo**

**1. Clone Repository:**
```powershell
git clone https://github.com/g0ochoa/python-mariachi-website.git
cd python-mariachi-website
```

**2. Create Virtual Environment:**
```powershell
python -m venv mariachi-env
```

**3. Activate Virtual Environment:**

**Windows:**
```powershell
mariachi-env\Scripts\activate
```

**Mac/Linux:**
```bash
source mariachi-env/bin/activate
```

**4. Install Dependencies:**
```powershell
pip install -r requirements.txt
```

**5. Create Your .env File:**
```powershell
# Copy the template
cp .env.example .env

# Edit .env and fill in values (use any text editor)
```

**6. Run Migrations:**
```powershell
python manage.py migrate
```

**7. Create Your Superuser:**
```powershell
python manage.py createsuperuser
# Enter your username, email, password
```

**8. Fix Your User Role:**
```powershell
python manage.py runserver
# Visit http://localhost:8000/admin
# Login with your credentials
# Go to Users → Click your username
# Change Role from "customer" to "admin"
# Click Save
```

**9. Verify Setup:**
```powershell
# Test the server
python manage.py runserver

# Visit http://localhost:8000/admin
# You should see Users in the sidebar
# You should be able to add/edit users
```

**10. Create Feature Branch:**
```powershell
git checkout -b feature/your-name/your-feature
```

---

## 🔧 **Common Issues & Solutions**

### **Issue 1: "No module named 'django'"**

**Problem:** Django not installed  
**Solution:**
```powershell
# Ensure virtual environment is activated
mariachi-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **Issue 2: "SECRET_KEY not found"**

**Problem:** Missing .env file  
**Solution:**
```powershell
# Copy template
cp .env.example .env

# Edit .env and add SECRET_KEY
```

### **Issue 3: "AUTH_USER_MODEL must be of the form 'app.ModelName'"**

**Problem:** Set AUTH_USER_MODEL after migrations ran  
**Solution:**
```powershell
# Delete database
rm db.sqlite3

# Delete migrations
rm accounts/migrations/0*.py

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### **Issue 4: "Users don't show in admin"**

**Problem:** User model not registered in admin.py  
**Solution:**
- Add `@admin.register(User)` decorator in accounts/admin.py
- Restart dev server

### **Issue 5: "Port 8000 already in use"**

**Problem:** Another server running on port 8000  
**Solution:**
```powershell
# Use different port
python manage.py runserver 8001

# Or kill existing process (Windows)
netstat -ano | findstr :8000
taskkill /PID [process_id] /F
```

### **Issue 6: Migration conflicts**

**Problem:** Migration files out of sync with database  
**Solution:**
```powershell
# Reset migrations (development only!)
python manage.py migrate accounts zero
python manage.py migrate
```

---

## 🎯 **Next Steps**

### **Immediate (Sprint 2)**
- [ ] Create basic views for public_site (home page)
- [ ] Set up URL routing
- [ ] Create templates folder structure
- [ ] Add static files (CSS, JavaScript)
- [ ] Create Score model in musicians_portal
- [ ] Test HTMX integration

### **Short-term (Sprint 3)**
- [ ] Build public website pages (home, about, gallery, contact)
- [ ] Implement customer registration form
- [ ] Create booking request system
- [ ] Design musicians portal UI
- [ ] Implement score library with search/filter

### **Long-term (Sprint 4+)**
- [ ] Migrate to PostgreSQL
- [ ] Implement Google Workspace SSO for musicians
- [ ] Build practice tools (metronome, audio recorder)
- [ ] Create event calendar
- [ ] Add promo code system
- [ ] Deploy to Google Cloud Platform

---

## 📚 **Additional Resources**

**Official Documentation:**
- Django Docs: https://docs.djangoproject.com/
- Django Tutorial: https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- HTMX Docs: https://htmx.org/docs/

**Team Resources:**
- GitHub Repository: https://github.com/g0ochoa/python-mariachi-website
- Project Documentation: `docs/` folder
- Architecture Docs: `docs/architecture/system-architecture.md`

---

## ✅ **Checklist for Verification**

After completing setup, verify these work:

- [ ] Virtual environment activated
- [ ] Django installed (`python -m django --version`)
- [ ] Server starts without errors
- [ ] Admin accessible at `/admin`
- [ ] Can login with superuser credentials
- [ ] Users visible in admin sidebar
- [ ] Can create new users
- [ ] Can edit user roles
- [ ] Database file exists (`db.sqlite3`)
- [ ] Requirements.txt present
- [ ] .env file created (not committed to Git)

---

**Questions or Issues?**  
Contact: Gerry Ochoa (@gerry in Teams)  
Sprint: Sprint 2 (Dec 2-8, 2025)  
Next Meeting: Monday, December 9, 2025

---

*This guide will be updated as the project evolves. Last updated: December 1, 2025*
