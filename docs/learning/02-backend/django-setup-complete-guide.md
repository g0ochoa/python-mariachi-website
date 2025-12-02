# Django Project Setup - Learning Guide
**Understanding Django Architecture and Project Initialization**

*Author: Gerry Ochoa*  
*Date: December 1, 2025*  
*Sprint: Sprint 2, Day 1 (Dec 1-7, 2025)*  
*Purpose: Educational resource explaining Django concepts and our implementation decisions*

---

## 📚 **Table of Contents**

1. [What This Guide Is](#what-this-guide-is)
2. [Project Structure Overview](#project-structure-overview)
3. [What We Built](#what-we-built)
4. [Understanding Django Components](#understanding-django-components)
5. [Common Pitfalls & Learning Points](#common-pitfalls--learning-points)
6. [Key Takeaways](#key-takeaways)
7. [Additional Learning Resources](#additional-learning-resources)
8. [What We Accomplished](#what-we-accomplished)

---

## 📖 **What This Guide Is**

This is a **learning resource**, not a setup tutorial. It explains:
- **What we did** during Django project initialization
- **Why we made** specific architectural decisions
- **How Django works** under the hood
- **What each command does** and why it matters

**Looking for setup instructions?** See `SPRINT_2_DAY_1_SUMMARY.md` in the root folder.

---

## 🏗️ **Project Structure Overview**

### **Our Final Structure**
```
python-mariachi-website/
├── manage.py                      # Django's command-line tool
├── requirements.txt               # Python dependencies list
├── .env                          # Secrets (NOT in Git)
├── .env.example                  # Template (IN Git)
├── db.sqlite3                    # SQLite database (NOT in Git)
├── mariachi_todo_terreno/        # Project configuration folder
│   ├── settings.py               # All project settings
│   ├── urls.py                   # URL routing map
│   ├── wsgi.py / asgi.py        # Server configs
├── accounts/                     # Authentication app
│   ├── models.py                 # User model
│   ├── admin.py                  # Admin config
│   ├── migrations/               # Database versions
├── public_site/                  # Public website app
└── musicians_portal/             # Private portal app
```

### **Understanding the Architecture**

**Why this structure?**
- **Monolithic design**: One project, multiple apps (not microservices)
- **Apps as siblings**: Apps sit next to project folder, not inside it
- **Separation of concerns**: Each app handles specific domain (accounts, public, private)

---

## 🔨 **What We Built**

### **1. Django Package Installation**

**Command Used:**
```powershell
pip install django psycopg2-binary python-dotenv django-htmx
```

**What Each Package Does:**

| Package | Purpose | Why Essential |
|---------|---------|---------------|
| `django` 5.2.8 | Web framework | Full MVC framework with ORM, admin, auth |
| `psycopg2-binary` 2.9.11 | PostgreSQL adapter | Future PostgreSQL migration |
| `python-dotenv` 1.2.1 | Environment vars | Keeps secrets out of source code |
| `django-htmx` 1.27.0 | HTMX integration | Modern UX without full page reloads |

**Key Concept - Dependency Management:**
- `pip install` downloads and installs packages
- `pip freeze > requirements.txt` saves exact versions
- Team installs with `pip install -r requirements.txt`
- Ensures everyone has identical environment

---

### **2. Django Project Creation**

**Command Used:**
```powershell
django-admin startproject mariachi_todo_terreno .
```

**Breaking It Down:**
- `django-admin` - Django's CLI tool (comes with Django package)
- `startproject` - Creates new project scaffold
- `mariachi_todo_terreno` - Project name (use underscores, not hyphens)
- `.` - Create in current directory (don't nest in subfolder)

**What Got Created:**
```
mariachi_todo_terreno/
├── __init__.py      # Python package marker
├── settings.py      # All configuration (DB, apps, security)
├── urls.py          # URL → view mapping
├── wsgi.py          # Production server interface
└── asgi.py          # Async server interface

manage.py            # Local development CLI tool
```

**Important Distinction:**
- **Project** = Configuration hub (settings, URLs, deployment)
- **Apps** = Feature modules (created next)
- One project can have many apps

---

### **3. Django Apps Creation**

**Commands Used:**
```powershell
python manage.py startapp accounts
python manage.py startapp public_site
python manage.py startapp musicians_portal
```

**What `startapp` Does:**
Creates self-contained module with standard structure:
```
app_name/
├── models.py      # Database schema (tables, fields)
├── views.py       # Request handlers (business logic)
├── admin.py       # Admin interface registration
├── apps.py        # App configuration
├── tests.py       # Unit tests
└── migrations/    # Database version history
```

**Our Three Apps:**

**`accounts`** - Authentication System
- Custom User model with roles (customer/musician/admin)
- Handles registration, login, permissions
- Shared by both public and private sites

**`public_site`** - Customer-Facing Website
- Home page, gallery, about
- Customer registration with promo opt-in
- Booking request forms

**`musicians_portal`** - Private Band Portal
- Score library (994+ songs)
- Practice tools (metronome, recorder)
- Event calendar, file sharing
- Musician-only access

**Key Architectural Decision:**
Apps are **siblings** to project folder, not nested inside:
```
✅ CORRECT:
project/
├── mariachi_todo_terreno/  ← Config
├── accounts/               ← App
├── public_site/            ← App
└── musicians_portal/       ← App

❌ WRONG:
mariachi_todo_terreno/
├── settings.py
└── accounts/               ← Don't nest apps
```

---

### **4. Django Settings Configuration**

**File Modified:** `mariachi_todo_terreno/settings.py`

**Changes Made:**

**A. Environment Variable Loading**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file into environment
```

**Why:** Keeps secrets (SECRET_KEY, passwords) out of source code

**B. App Registration**
```python
INSTALLED_APPS = [
    'django.contrib.admin',      # Admin interface
    'django.contrib.auth',       # Authentication
    'django.contrib.contenttypes',  # Content types
    'django.contrib.sessions',   # Session management
    'django.contrib.messages',   # Flash messages
    'django.contrib.staticfiles', # CSS/JS/images
    'django_htmx',               # Third-party
    'accounts',                  # Our apps
    'public_site',
    'musicians_portal',
]
```

**Why Order Matters:**
1. Django built-ins first (always required)
2. Third-party packages
3. Your local apps last (can depend on above)

**C. Custom User Model Declaration**
```python
AUTH_USER_MODEL = 'accounts.User'
```

**⚠️ CRITICAL DECISION:**
- Must be set **BEFORE** first migration
- Can't easily change after migrations run
- Even if you don't need custom fields initially, do it anyway
- Django docs strongly recommend this

**D. Environment-Based Secrets**
```python
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-value')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

**Why:** Production uses different values than development

---

### **5. Custom User Model Implementation**

**File Created:** `accounts/models.py`

**Our User Model:**
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('musician', 'Musician'),
        ('admin', 'Administrator'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )
    
    # Customer fields
    phone = models.CharField(max_length=20, blank=True)
    promo_opt_in = models.BooleanField(default=False)
    
    # Musician fields  
    instrument = models.CharField(max_length=50, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
```

**Key Concepts:**

**AbstractUser vs AbstractBaseUser:**
- `AbstractUser` extends Django's built-in User (easier)
- Keeps username, password, email, is_staff, is_active
- Just adds our custom fields on top

**Field Type Explanations:**

| Field Type | What It Stores | Example Use |
|------------|----------------|-------------|
| CharField | Text (fixed max length) | phone, instrument |
| BooleanField | True/False | promo_opt_in |
| choices= | Dropdown options | role selection |
| blank=True | Optional in forms | phone not required |
| null=True | Can be NULL in DB | instrument nullable |
| unique=True | No duplicates | google_id unique |
| default= | Value if not provided | role='customer' |

**Design Decision - Single User Model:**
- One model with role field vs multiple models (Customer, Musician)
- Simpler authentication (single login table)
- Easier permissions (check role field)
- Fields can be nullable for unused roles

---

### **6. Database Migrations**

**Commands Used:**
```powershell
python manage.py makemigrations  # Create migration file
python manage.py migrate         # Apply to database
```

**What Migrations Are:**
Think of them as "Git commits for your database schema"

**The Workflow:**
```
1. Change models.py
   └─► Add/modify fields

2. makemigrations
   └─► Creates Python file with instructions
   └─► Example: accounts/migrations/0001_initial.py

3. migrate
   └─► Executes SQL commands
   └─► Creates/modifies actual database tables

4. Database updated
   └─► Schema matches your models
```

**Why This System?**
- Version control for database structure
- Team can sync database changes
- Can roll back if needed
- Django tracks what's been applied

**Our First Migration:**
- Created `accounts_user` table
- All AbstractUser fields (username, password, email, etc.)
- Our custom fields (role, phone, promo_opt_in, instrument, google_id)
- Plus Django's built-in tables (admin, sessions, permissions)

**Total: 19 migrations applied** (accounts + Django built-ins)

---

### **7. Superuser Creation**

**Command Used:**
```powershell
python manage.py createsuperuser
```

**What It Does:**
- Creates User record in database
- Sets `is_staff = True` (can access admin)
- Sets `is_superuser = True` (all permissions)
- Hashes password with PBKDF2 (never stores plain text)
- Role defaults to 'customer' (must change manually)

**Security Note:**
Django uses PBKDF2 password hashing with SHA256:
- 320,000 iterations (as of Django 4.2+)
- Salted (prevents rainbow table attacks)
- Even if database is compromised, passwords are safe

---

### **8. Django Admin Registration**

**File Created:** `accounts/admin.py`

**The Code:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', ...)
    list_filter = ('role', 'is_staff', ...)
    search_fields = ('username', 'email', ...)
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
        ('Customer Information', {'fields': ('phone', 'promo_opt_in')}),
        ('Musician Information', {'fields': ('instrument', 'google_id')}),
    )
```

**What `@admin.register(User)` Does:**
- Makes model visible in admin sidebar
- Without this, model exists in database but is **invisible** in admin
- Common beginner mistake

**Extending UserAdmin:**
- `UserAdmin` has Django's default config
- We extend it with `+` operator
- Adds our custom fieldsets to existing ones
- Keeps all built-in functionality

---

### **9. Requirements File Generation**

**Command Used:**
```powershell
pip freeze > requirements.txt
```

**What It Does:**
- Lists ALL installed packages
- Includes exact version numbers
- Output example:
```
Django==5.2.8
django-htmx==1.27.0
psycopg2-binary==2.9.11
python-dotenv==1.2.1
sqlparse==0.5.4
tzdata==2025.2
asgiref==3.11.0
```

**Why Version Locking Matters:**
- Package updates can break code
- Team needs identical versions
- `pip install -r requirements.txt` installs exact versions
- Production matches development

---

### **10. Environment Variable Setup**

**Files Created:**

**`.env.example`** (Template - IN Git)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**`.env`** (Actual Secrets - NOT in Git)
```env
SECRET_KEY=django-insecure-u@c!plx5_x3uya-cmt9ko%s*iyz8#q6p74k2$1!gwzdjbpzlkf
DEBUG=True
```

**The Pattern:**
- `.env.example` shows required variables (no real values)
- `.env` has actual secrets (in .gitignore)
- Team copies example to .env and fills in values
- Production has different .env (different SECRET_KEY, DEBUG=False)

**Why This Matters:**
- Secrets never in source control
- Each environment (dev/staging/prod) has own values
- Same code runs everywhere with different config

---

## 🧠 **Understanding Django Components**

Now that we've built our Django project, let's understand how the pieces fit together.

### **The MVT Pattern (Model-View-Template)**

Django uses **Model-View-Template** (MVT) architecture:

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Model   │◄────►│   View   │◄────►│ Template │
│(Database)│      │ (Logic)  │      │  (HTML)  │
└──────────┘      └──────────┘      └──────────┘
     │                  │                  │
     │                  │                  │
  models.py         views.py         templates/
```

**Model** - Database structure (what data we store)  
- Defines tables, fields, relationships
- Provides Python API for querying data
- Example: User model with username, email, role

**View** - Business logic (what happens when user visits a page)  
- Handles HTTP requests
- Queries database through models
- Renders templates with data
- Example: Function that fetches scores and displays them

**Template** - HTML presentation (what user sees)  
- HTML with Django template language
- Displays data from views
- Loops, conditionals, filters
- Example: HTML page showing list of scores

**Why Separate These?**
- **Maintainability**: Change database without touching HTML
- **Reusability**: Same model used by multiple views
- **Team collaboration**: Database designers, backend devs, frontend devs work independently

---

### **Django Request/Response Flow**

Understanding how Django handles a web request:

```
1. User visits URL
   ↓
   http://localhost:8000/musicians/scores/

2. Django checks urls.py
   ↓
   path('musicians/scores/', views.score_library)

3. View function executes
   ↓
   scores = Score.objects.filter(user=request.user)

4. View renders template
   ↓
   return render(request, 'scores.html', {'scores': scores})

5. Template generates HTML
   ↓
   {% for score in scores %}
     <div>{{ score.title }}</div>
   {% endfor %}

6. Browser displays page
   ↓
   User sees their scores
```

**Key Concepts:**
- **URL patterns** are checked in order (first match wins)
- **Views** are Python functions or classes
- **Templates** receive context (dictionary of variables)
- **ORM** (Object-Relational Mapping) converts Python to SQL

---

###  **Migration Workflow**

Migrations are version control for your database schema:

```
1. Developer changes model
   └─► models.py: Add role = models.CharField(...)

2. Django detects changes
   └─► python manage.py makemigrations
       Analyzes model changes
       Creates migration file (0002_user_role.py)

3. Migration file contains operations
   └─► migrations.AddField(
          model_name='user',
          name='role',
          field=models.CharField(...)
       )

4. Apply migration to database
   └─► python manage.py migrate
       Executes SQL: ALTER TABLE accounts_user ADD role VARCHAR(20)

5. Database schema updated
   └─► Table now has new 'role' column
       All existing users get default value ('customer')
```

**Why Migrations Matter:**
- **Version control**: Track database changes over time
- **Team collaboration**: Share schema changes via Git
- **Rollback capability**: Can undo migrations (in development)
- **Documentation**: Migration files show schema evolution

**Migration Dependency Graph:**
```
0001_initial.py (create User table)
    ↓
0002_user_role.py (add role field)
    ↓
0003_user_instrument.py (add instrument field)
```

Each migration depends on the previous one. Django tracks which migrations have been applied.

---

### **App Structure Explained**

Each Django app follows consistent structure:

```
accounts/
├── migrations/           # Database version history
│   ├── 0001_initial.py  # Creates User table
│   ├── 0002_add_role.py # Adds role field
│   └── __init__.py
├── __init__.py          # Makes this a Python package
├── admin.py             # Register models in /admin interface
├── apps.py              # App configuration
├── models.py            # Database models (classes = tables)
├── views.py             # Request handlers (functions = pages)
├── tests.py             # Unit tests
└── urls.py              # URL routing (optional, create manually)
```

**When to Create a New App:**

✅ **Create new app when:**
- Feature is self-contained and reusable
- Has its own models/database tables
- Can be developed independently
- Could potentially be used in other projects
- Examples: blog app, payment app, notification system

❌ **Add to existing app when:**
- Feature extends existing functionality
- Shares models with existing app
- Tightly coupled to app's purpose
- Small utility functions
- Examples: add password reset to accounts, add search to scores

**Our App Decision Reasoning:**

**`accounts`** - Separate app because:
- Authentication is core functionality
- User model used by all other apps
- Could be reused in future projects
- Clear, focused purpose

**`public_site`** - Separate app because:
- Completely different audience (public vs members)
- No shared models with musicians_portal
- Different permissions (anonymous vs authenticated)
- Could be developed independently

**`musicians_portal`** - Separate app because:
- Private functionality requiring authentication
- Complex models (scores, practice sessions, events)
- Specific to musicians role
- Clear boundary from public site

---

## 🚨 **Common Pitfalls & Learning Points**

These are mistakes developers commonly make when starting with Django. Understanding why they happen helps you avoid them.

### **Pitfall 1: Forgetting Virtual Environment**

**Why It Matters:**  
Without activating the virtual environment, packages install globally and can cause conflicts.

**Learning:**  
- Virtual environments isolate project dependencies
- Always verify `(mariachi-env)` appears in your terminal prompt
- Global installations pollute system Python and cause version conflicts

**Conceptual Understanding:**  
Python's virtual environments create isolated Python interpreters. When activated, `pip install` modifies only that environment's `site-packages` directory, not the system-wide location.

---

### **Pitfall 2: Missing SECRET_KEY in Production**

**Why It Matters:**  
Django's SECRET_KEY protects cryptographic signing. Hardcoding it exposes security vulnerabilities.

**Learning:**  
- SECRET_KEY must be unique per environment
- Never commit secret keys to version control
- Environment variables separate config from code (12-factor app principle)

**Conceptual Understanding:**  
The SECRET_KEY is used for:
- Session cookie signing (prevents tampering)
- CSRF token generation
- Password reset tokens
- Any cryptographic signing in Django

If exposed, attackers can forge sessions and bypass security measures.

---

### **Pitfall 3: Setting AUTH_USER_MODEL After First Migration**

**Why It Matters:**  
Django bakes AUTH_USER_MODEL into database foreign keys. Changing it after migrations requires database reset.

**Learning:**  
- Custom user models must be configured BEFORE first `migrate`
- Database relationships are hard to change once created
- Always plan authentication early in project

**Conceptual Understanding:**  
When Django creates tables, it creates foreign keys pointing to `auth_user` (default) or your custom user table. These relationships are stored in the database schema. Changing AUTH_USER_MODEL later would require:
1. Dropping all tables with user foreign keys
2. Recreating migrations
3. Losing all data

This is why Django documentation emphasizes: "It's highly recommended to set up a custom user model, even if the default User model is sufficient for you."

---

### **Pitfall 4: Forgetting to Register Models in Admin**

**Why It Matters:**  
Django admin doesn't automatically discover models. Registration is explicit.

**Learning:**  
- Python's "explicit is better than implicit" philosophy
- The `@admin.register()` decorator tells Django to include the model
- Admin customization happens through ModelAdmin classes

**Conceptual Understanding:**  
Django's admin is dynamically generated. When you visit `/admin`, Django:
1. Checks `admin.py` files in all installed apps
2. Finds registered models
3. Generates CRUD interfaces using model metadata

Without registration, Django doesn't know you want that model in admin.

---

### **Pitfall 5: Port Already in Use**

**Why It Matters:**  
Only one process can bind to a port. Helps understand web server basics.

**Learning:**  
- Web servers listen on specific ports (8000 for dev)
- Operating systems prevent port conflicts
- Development servers run single-threaded (unlike production)

**Conceptual Understanding:**  
When `runserver` starts, it attempts to bind to `0.0.0.0:8000`. If another process already bound that port, the OS returns "Address already in use" error. This teaches:
- Ports are OS-level resources
- One server per port
- Production uses reverse proxies (nginx) to route multiple apps

---

### **Pitfall 6: Migration Conflicts**

**Why It Matters:**  
Migrations are version control for your database schema. Conflicts happen in team environments.

**Learning:**  
- Migrations track schema changes over time
- Each migration depends on previous ones (linked list structure)
- Team coordination prevents conflicts

**Conceptual Understanding:**  
Django migrations form a dependency graph:
```
0001_initial.py → 0002_add_role_field.py → 0003_add_indexes.py
```

If two developers create migrations simultaneously:
```
Developer A: 0001 → 0002_add_email
Developer B: 0001 → 0002_add_phone
```

Merge conflict! Both named `0002`. Solution: Django's migration system allows squashing or manual renumbering.

---

## 💡 **Key Takeaways**

1. **Virtual Environments Are Non-Negotiable**  
   Treat them like version control - essential, not optional.

2. **Security Configuration Belongs in Environment Variables**  
   Code is public, config is private.

3. **Plan Authentication Early**  
   AUTH_USER_MODEL cannot be easily changed later.

4. **Django Admin Is Explicit, Not Magic**  
   Registration, customization, permissions all require code.

5. **Development vs Production Are Different Worlds**  
   Dev server is single-threaded, no security hardening, debug mode on.

6. **Migrations Are Team Coordination Tools**  
   Communicate schema changes, review migration files like code.

---

## 📚 **Additional Learning Resources**

**Official Django Documentation:**
- [Django Documentation](https://docs.djangoproject.com/) - Comprehensive reference
- [Django Tutorial Series](https://docs.djangoproject.com/en/5.2/intro/tutorial01/) - Official step-by-step tutorial
- [Django Models Reference](https://docs.djangoproject.com/en/5.2/topics/db/models/) - Deep dive into ORM
- [Django Authentication](https://docs.djangoproject.com/en/5.2/topics/auth/) - User authentication system

**Understanding Web Frameworks:**
- [12-Factor App Methodology](https://12factor.net/) - Modern app development principles (explains environment variables, config)
- [MVT vs MVC](https://docs.djangoproject.com/en/5.2/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) - Django's architecture explained

**Python Virtual Environments:**
- [Python venv Documentation](https://docs.python.org/3/library/venv.html) - Official virtual environment guide
- [Real Python - Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/) - Practical guide

**Database Migrations:**
- [Django Migrations Guide](https://docs.djangoproject.com/en/5.2/topics/migrations/) - How migrations work
- [Understanding Django Migrations](https://realpython.com/django-migrations-a-primer/) - Real Python tutorial

**HTMX for Modern UIs:**
- [HTMX Documentation](https://htmx.org/docs/) - Official HTMX guide
- [django-htmx Package](https://django-htmx.readthedocs.io/) - Django integration

---

## 🎯 **What We Accomplished**

By completing this Django setup, we've established:

**Technical Foundation:**
- ✅ Custom user authentication system (role-based access control ready)
- ✅ Three Django apps (modular architecture for different features)
- ✅ Database schema with migrations (version-controlled database changes)
- ✅ Admin interface (rapid development and data management)
- ✅ Security configuration (environment variables, secret key management)
- ✅ Modern frontend tools (HTMX for dynamic UIs without JavaScript frameworks)

**Development Best Practices:**
- ✅ Virtual environment isolation (dependency management)
- ✅ Requirements file (reproducible environments)
- ✅ Git version control (code history and collaboration)
- ✅ Environment-based configuration (separation of code and config)

**Project Understanding:**
- ✅ Why Django uses MVT pattern (separation of concerns)
- ✅ How migrations work (database versioning)
- ✅ Why custom user models matter (future-proofing authentication)
- ✅ How Django admin accelerates development (automatic CRUD interfaces)

**Ready for Next Phase:**
We can now build views, templates, and business logic knowing our foundation is solid.

---
- [ ] Users visible in admin sidebar
- [ ] Can create new users
- [ ] Can edit user roles
- [ ] Database file exists (`db.sqlite3`)
- [ ] Requirements.txt present
- [ ] .env file created (not committed to Git)

---

**Questions or Issues?**  
Contact: Gerry Ochoa (@gerry in Teams)  
Sprint: Sprint 2 (Dec 1-7, 2025)  
Next Meeting: Monday, December 8, 2025

---

*This guide will be updated as the project evolves. Last updated: December 1, 2025*
