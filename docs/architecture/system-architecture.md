# System Architecture - Mariachi Todo Terreno Website
*High-level architecture and technical design*

**Last Updated**: November 30, 2025  
**Status**: Initial Design Phase

---

## 🎯 Architecture Overview

This is a **monolithic Django application** with two distinct sections (public website + private portal) deployed to Google Cloud Platform.

### **Architecture Pattern**
- **Monolithic Application** (not microservices)
- **Server-Side Rendering** (Django templates)
- **Progressive Enhancement** (HTMX for interactivity)
- **Relational Database** (PostgreSQL)

### **Why Monolithic?**
✅ Simpler deployment (one application)  
✅ Easier development (one codebase)  
✅ Better for small teams (4 people)  
✅ Sufficient for expected traffic  
✅ Can scale vertically on GCP

---

## 🏗️ Application Structure

### **Django Project Layout**

```
mariachi_todo_terreno/           # Django project root
├── mariachi_todo_terreno/       # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config (future websockets)
├── public_site/                 # Public website app
│   ├── models.py                # Events, Videos, Bookings
│   ├── views.py                 # Public views
│   ├── urls.py                  # Public URLs
│   └── templates/               # Public templates
│       ├── home.html
│       ├── about.html
│       ├── gallery.html
│       └── contact.html
├── musicians_portal/            # Private musicians app
│   ├── models.py                # Scores, Practice Sessions
│   ├── views.py                 # Portal views
│   ├── urls.py                  # Portal URLs
│   └── templates/               # Portal templates
│       ├── dashboard.html
│       ├── scores/
│       │   ├── library.html
│       │   ├── detail.html
│       │   └── search_results.html (HTMX partial)
│       └── practice/
│           ├── calendar.html
│           └── session.html
├── accounts/                    # Authentication app
│   ├── models.py                # Custom User model
│   ├── views.py                 # Login, logout, SSO
│   ├── urls.py                  # Auth URLs
│   └── backends.py              # Google SSO backend
├── static/                      # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── media/                       # Uploaded files (scores, videos)
│   ├── scores/
│   └── videos/
└── templates/                   # Base templates
    └── base.html                # Main layout template
```

---

## 📊 Database Schema (PostgreSQL)

### **Core Models**

#### **1. User Management**
```
User (Django AbstractUser)
├── id (PK)
├── email (unique)
├── first_name
├── last_name
├── is_musician (boolean)
├── role (choices: ADMIN, MUSICIAN)
├── google_workspace_id
└── date_joined

MusicianProfile (extends User)
├── user (FK to User)
├── instrument
├── phone
└── bio
```

#### **2. Public Site Models**
```
Event
├── id (PK)
├── title
├── date
├── venue
├── description
├── is_public (boolean)
└── created_by (FK to User)

Video
├── id (PK)
├── title
├── url
├── thumbnail
├── description
└── upload_date

BookingRequest
├── id (PK)
├── customer_name
├── customer_email
├── event_date
├── venue
├── message
├── status (choices: PENDING, APPROVED, REJECTED)
└── created_at
```

#### **3. Musicians Portal Models**
```
Score
├── id (PK)
├── title
├── composer
├── arranger
├── genre (choices: RANCHERA, BOLERO, CUMBIA, etc.)
├── key_signature
├── time_signature
├── tempo
├── difficulty (1-5)
├── pdf_file (FileField)
├── tags (ManyToMany to Tag)
├── uploaded_by (FK to User)
└── created_at

Tag
├── id (PK)
└── name (unique)

PracticeSession
├── id (PK)
├── date
├── location
├── notes
├── scores_practiced (ManyToMany to Score)
├── attendees (ManyToMany to User)
└── created_by (FK to User)

Recording
├── id (PK)
├── session (FK to PracticeSession)
├── audio_file (FileField)
├── title
├── uploaded_by (FK to User)
└── created_at
```

---

## 🔄 Request Flow

### **Public Website Request (Traditional)**
```
1. User visits: https://mariachitodoterreno.com/gallery
2. Browser → Nginx → Django
3. Django views.py: render('gallery.html', {'videos': videos})
4. Django renders full HTML page
5. Django → Nginx → Browser
6. Browser displays page
```

### **Musicians Portal with HTMX (Modern)**
```
1. Musician types in search box
2. HTMX intercepts, sends: GET /portal/scores/search/?q=cielito
3. Browser → Nginx → Django
4. Django views.py: render('scores/search_results.html', {'scores': scores})
5. Django renders ONLY results HTML (partial)
6. Django → Nginx → Browser
7. HTMX swaps ONLY #results div (no page reload)
```

---

## 🎨 Frontend Architecture

### **Technology Stack**
- **Django Templates** - Server-side HTML generation
- **HTMX** - Dynamic interactivity without page reloads
- **CSS** - Styling (possibly Tailwind or Bootstrap)
- **Vanilla JavaScript** - Where needed (metronome, audio recorder)

### **HTMX Integration Pattern**

**Example: Score Library Search**

```html
<!-- templates/musicians_portal/scores/library.html -->
<div class="score-library">
    <form hx-get="/portal/scores/search/" 
          hx-trigger="keyup changed delay:500ms"
          hx-target="#results"
          hx-indicator="#loading">
        <input type="text" name="q" placeholder="Search songs...">
        <select name="genre">
            <option value="">All Genres</option>
            <option value="ranchera">Ranchera</option>
            <option value="bolero">Bolero</option>
        </select>
    </form>
    
    <div id="loading" class="htmx-indicator">Loading...</div>
    
    <div id="results">
        {% include 'scores/search_results.html' %}
    </div>
</div>
```

```html
<!-- templates/musicians_portal/scores/search_results.html -->
<!-- HTMX partial - only this gets swapped -->
{% for score in scores %}
    <div class="score-card">
        <h3>{{ score.title }}</h3>
        <p>{{ score.composer }} - {{ score.genre }}</p>
        <a hx-get="/portal/scores/{{ score.id }}/detail/" 
           hx-target="#modal"
           hx-swap="innerHTML">View</a>
    </div>
{% endfor %}
```

### **When to Use HTMX vs Traditional**
- ✅ **HTMX**: Score search, filters, live updates, modals
- ✅ **Traditional**: Static pages (about, contact), initial page loads
- ✅ **Vanilla JS**: Audio recording, metronome, file upload previews

---

## 🔐 Authentication Flow

### **Google Workspace SSO**

```
1. User clicks "Login with Google"
2. Django redirects to Google OAuth
3. User authenticates with Google
4. Google redirects back with auth code
5. Django verifies user is in Mariachi Todo Terreno workspace
6. Django creates/updates User record
7. Django creates session
8. User redirected to musicians portal dashboard
```

### **Authorization Levels**
- **Public**: Anyone (no auth)
- **Musician**: Authenticated band member (read scores, view calendar)
- **Admin**: Gerry (upload scores, manage users, approve bookings)

---

## ☁️ Deployment Architecture (GCP)

### **Production Infrastructure**

```
Internet
    ↓
Cloud Load Balancer (HTTPS)
    ↓
Cloud Run (Django Application)
    ├→ Cloud SQL (PostgreSQL)
    ├→ Cloud Storage (Media files: scores, videos)
    └→ Secret Manager (Environment variables)
```

### **Environments**
1. **Local Development** - SQLite (for quick setup), then PostgreSQL
2. **Staging** - GCP Cloud Run + Cloud SQL (small instance)
3. **Production** - GCP Cloud Run + Cloud SQL (auto-scaling)

### **Why Cloud Run?**
- ✅ Pay only for what you use (band website = low traffic)
- ✅ Auto-scales to zero (save money)
- ✅ Built-in HTTPS
- ✅ Easy deployment (Docker container)
- ✅ No server management

---

## 📈 Scalability Considerations

### **Expected Traffic**
- **Public Site**: ~100-500 visitors/month (mariachi booking inquiries)
- **Musicians Portal**: 4-10 active users (band members)
- **Peak Times**: Weekend evenings (people booking events)

### **Scaling Strategy**
1. **Phase 1** (Current): Single Cloud Run instance (sufficient)
2. **Phase 2** (If grows): Auto-scale Cloud Run (up to 5 instances)
3. **Phase 3** (Future): CDN for static assets (Cloud CDN)

**Reality Check**: Mariachi band website won't have scaling issues. Architecture is over-engineered for learning purposes.

---

## 🔒 Security Architecture

### **Security Layers**
1. **Network**: HTTPS only, Cloud Load Balancer
2. **Application**: Django security middleware (CSRF, XSS, Clickjacking)
3. **Authentication**: Google SSO (no password storage)
4. **Authorization**: Role-based access (Admin vs Musician)
5. **Data**: PostgreSQL with encrypted connections
6. **Files**: Signed URLs for score downloads (Cloud Storage)

### **Zero Trust Principles**
- ❌ No implicit trust (verify every request)
- ✅ Least privilege (musicians can't delete scores)
- ✅ Audit logging (track who accessed what)
- ✅ Session timeouts (auto-logout after inactivity)

---

## 📦 Technology Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Framework** | Django 5.x | Full-featured, secure, great for learning |
| **Database** | PostgreSQL 15+ | Relational data, GCP integration |
| **Frontend** | Django Templates + HTMX | Modern UX, simple deployment |
| **Auth** | Google Workspace SSO | Secure, no password management |
| **Hosting** | GCP Cloud Run | Serverless, cost-effective |
| **Storage** | Cloud Storage | Scalable file storage |
| **IaC** | Terraform | Version-controlled infrastructure |

---

## 🚀 Development Phases

### **Phase 1: Foundation** (Current Sprint)
- Django project setup
- PostgreSQL connection
- Basic authentication
- Project structure

### **Phase 2: Public Site**
- Home, About, Gallery, Contact pages
- Booking request form
- Responsive design

### **Phase 3: Musicians Portal**
- Score library (main feature)
- Search and filters (HTMX)
- File uploads

### **Phase 4: Advanced Features**
- Practice calendar
- Audio recording
- Event management

### **Phase 5: Production**
- GCP deployment
- Domain setup
- SSL/HTTPS
- Monitoring

---

*This architecture balances learning objectives with production requirements while keeping complexity manageable for a 4-person team.*
