# Python Mariachi Website
*Learning-Focused Full-Stack Python Development for Mariachi Todo Terreno*

## 🎯 Project Overview

This is a comprehensive Python web development project to create a professional website for Mariachi Todo Terreno. The project serves dual purposes: providing a real-world application for the mariachi band and offering hands-on learning experience in modern Python web development, security engineering, and DevOps practices.

## 🎵 About Mariachi Todo Terreno

Mariachi Todo Terreno is a professional mariachi group led by Gerry Ochoa (trumpet). This website will serve both business needs (customer engagement, bookings) and internal band management (practice coordination, music library, scheduling).

## 🏗️ Project Structure

```
python-mariachi-website/
├── README.md                      # This file
├── original-requirements.md       # Comprehensive project requirements
├── asana-project-breakdown.md     # Epic/Task breakdown for Asana
├── LEARNING_LOG.md                # Learning resources index
├── SPRINT_2_DAY_1_SUMMARY.md      # Latest sprint summary
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── manage.py                      # Django management tool
├── mariachi_todo_terreno/         # Django project configuration
│   ├── settings.py                # Project settings
│   ├── urls.py                    # URL routing
│   ├── wsgi.py                    # WSGI config
│   └── asgi.py                    # ASGI config
├── accounts/                      # Authentication app
│   ├── models.py                  # Custom User model
│   ├── admin.py                   # Admin configuration
│   ├── views.py                   # View logic
│   └── migrations/                # Database migrations
├── public_site/                   # Public-facing website app
├── musicians_portal/              # Private band member portal app
├── docs/                          # Documentation
│   ├── architecture/              # System design documents
│   │   └── system-architecture.md
│   ├── learning/                  # Learning guides by topic
│   │   ├── README.md              # Learning guide index
│   │   └── 02-backend/
│   │       └── django-setup-complete-guide.md
│   ├── sessions/                  # Development session logs
│   │   ├── session-01-2025-11-30.md
│   │   └── session-02-2025-12-01.md
│   └── website-design/            # Design research and mockups
└── mariachi-env/                  # Virtual environment (local only)
```

## 🛠️ Tech Stack (Current Implementation)

### Backend
- **Framework**: Django 5.2.8 ✅
- **Database**: SQLite (development) → PostgreSQL 15+ (production)
- **Authentication**: Custom User model with role-based access
- **Packages**: django-htmx 1.27.0, psycopg2-binary 2.9.11, python-dotenv 1.2.1
- **Python**: 3.13.7

### Frontend
- **Templates**: Django Template Language
- **Interactivity**: HTMX (Progressive enhancement)
- **Styling**: HTML5, CSS3, JavaScript (vanilla)
- **Design**: Mobile-first responsive design

### Infrastructure & DevOps
- **Cloud Platform**: Google Cloud Platform (planned)
- **Version Control**: GitHub
- **Environment Management**: Python virtual environments
- **Development Database**: SQLite
- **Production Database**: PostgreSQL (planned)

## 🎯 Learning Objectives

- Master Python web development frameworks
- Implement enterprise-grade security patterns
- Practice Infrastructure as Code (IaC) with Terraform
- Apply CI/CD methodologies in real projects
- Collaborate using Agile project management

## 🌐 Website Features

### Public Website
- Professional mariachi showcase
- Video gallery and performance media
- Event calendar and availability
- Customer registration with promo opt-in
- Booking request system
- Contact information

### Musicians Portal (Private)
- Secure authentication for band members
- Custom User model with role-based permissions
- Digital scores library (994+ songs planned)
- Practice scheduling and organization
- Member dashboard
- File sharing for recordings

### Django Admin Interface
- User management with role assignment
- Customer information tracking
- Musician profile management
- Content management capabilities

## 🚀 Development Approach

- **Agile Methodology**: Sprint-based development with Asana task management
- **Learning-Focused**: Prioritize understanding over speed
- **Security-First**: Enterprise security practices from day one
- **Documentation-Driven**: Comprehensive logging and knowledge sharing
- **Incremental Development**: Build and test features iteratively

## 📋 Current Status

**Sprint**: Sprint 2 (Dec 1-7, 2025) - Day 1 Complete ✅  
**Project Start**: November 24, 2025  
**Team**: Gerry Ochoa (Project Manager), Paco "Sensei" Cisneros, Carlos Cortes, Juan Marin  
**Meeting Schedule**: Mondays on Microsoft Teams  
**Next Meeting**: Monday, December 8, 2025

### Sprint 2 Progress (Week 2)
- [x] Django project created (mariachi_todo_terreno)
- [x] 3 Django apps created (accounts, public_site, musicians_portal)
- [x] Custom User model with role-based access (customer/musician/admin)
- [x] Database migrations created and applied
- [x] Django admin configured with User management
- [x] Superuser account created
- [x] Requirements.txt generated
- [x] Environment variables configured (.env, .env.example)
- [x] Comprehensive Django setup guide created
- [x] All code committed to GitHub (dev branch)

### Sprint 1 Completed (Nov 24-30)
- [x] Framework decision: Django
- [x] Database decision: PostgreSQL
- [x] Team assignments finalized
- [x] Project requirements documented
- [x] Repository initialized

### Current Team Assignments (Sprint 2)
- **Gerry Ochoa**: Django project setup ✅, Basic views and URL routing (next)
- **Paco "Sensei" Cisneros**: PostgreSQL configuration guide (due Dec 7)
- **Carlos Cortes**: Development environment setup (due Dec 7)
- **Juan Marin**: Frontend mockups for 4 pages (due Dec 7)

## 📚 Documentation

All project documentation is organized in `/docs/`:

- **[Learning Guides](docs/learning/README.md)**: Complete learning resources organized by topic
  - [Django Setup Guide](docs/learning/02-backend/django-setup-complete-guide.md) - Step-by-step Django installation
  - Foundations, Backend, Frontend, Database, DevOps, Security
- **[Architecture](docs/architecture/system-architecture.md)**: System design and technical architecture
- **[Original Requirements](original-requirements.md)**: Complete project specifications
- **[Asana Task Breakdown](asana-project-breakdown.md)**: Epic/Story/Task structure for project management
- **[Sprint Summaries](SPRINT_2_DAY_1_SUMMARY.md)**: Sprint progress and team updates

## 🚀 Quick Start for Team Members

1. **Clone repository**: `git clone https://github.com/g0ochoa/python-mariachi-website.git`
2. **Follow setup guide**: [Django Setup Complete Guide](docs/learning/02-backend/django-setup-complete-guide.md)
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Configure environment**: Copy `.env.example` to `.env`
5. **Run migrations**: `python manage.py migrate`
6. **Create superuser**: `python manage.py createsuperuser`
7. **Start server**: `python manage.py runserver`
8. **Access admin**: http://localhost:8000/admin

## 🔗 Related Projects

This project is part of the broader Mariachi Todo Terreno web presence, which includes:
- **HTML/CSS/JS Version**: Currently live production website
- **MEAN Stack Version**: Advanced application with Angular frontend
- **Python Version**: This learning-focused project

## 📞 Contact

**Project Manager**: Gerry Ochoa  
**Role**: Trumpet Player & Security Engineer  
**Experience**: Security Engineering since 2018

---

*This project emphasizes learning, security, and professional development while creating a real-world application for Mariachi Todo Terreno.*