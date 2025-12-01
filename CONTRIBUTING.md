# Contributing to Mariachi Todo Terreno Website

Welcome to the team! This guide will help you get started with the project.

## 🎯 Project Overview

We're building a professional website for Mariachi Todo Terreno using Django + PostgreSQL + HTMX. This is both a real production website AND a learning project.

**Team:**
- **Gerry Ochoa** - Project Manager, Django setup, backend development
- **Paco Cisneros** - PostgreSQL configuration, database architecture
- **Carlos Cortes** - Backend development support, security testing
- **Juan Marin** - Frontend design and mockups

## 🛠️ Tech Stack

- **Backend**: Django 5.x + Python 3.11+
- **Database**: PostgreSQL 15+
- **Frontend**: Django Templates + HTMX
- **Deployment**: Google Cloud Platform
- **Version Control**: Git + GitHub

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/g0ochoa/python-mariachi-website.git
cd python-mariachi-website
```

### 2. Set Up Python Environment

**Create virtual environment:**
```bash
python -m venv mariachi-env
```

**Activate virtual environment:**

*Windows (PowerShell):*
```powershell
.\mariachi-env\Scripts\Activate.ps1
```

*macOS/Linux:*
```bash
source mariachi-env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Requirements file will be created when we install Django)*

### 4. Set Up Database

**Option A: Start with SQLite (easier)**
- No setup needed, Django creates `db.sqlite3` automatically

**Option B: Use PostgreSQL (production-like)**
- Install PostgreSQL locally
- Create database: `createdb mariachi_db`
- Configure `.env` file (see `.env.example`)

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 📁 Project Structure

```
python-mariachi-website/
├── mariachi_todo_terreno/      # Django project
│   ├── settings.py             # Configuration
│   └── urls.py                 # URL routing
├── public_site/                # Public website app
├── musicians_portal/           # Musicians portal app
├── accounts/                   # Authentication app
├── docs/                       # Documentation
│   ├── architecture/           # System design
│   └── learning/               # Learning guides
├── static/                     # CSS, JS, images
├── templates/                  # Django templates
└── requirements.txt            # Python dependencies
```

## 🔄 Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `dev` - Development integration branch
- `feature/feature-name` - Individual features

### Making Changes

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request** on GitHub for review

### Commit Message Format

```
<type>: <description>

[optional body]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting (no logic change)
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add score search functionality to musicians portal
fix: Correct date formatting in event calendar
docs: Update README with HTMX examples
```

## 🧪 Testing

*(To be added when we set up tests)*

## 📚 Learning Resources

Check `docs/learning/` for topic-specific guides:
- Django Basics
- Django ORM
- HTMX Integration
- PostgreSQL
- Git & Version Control

## 💬 Communication

- **Meetings**: Weekly Mondays on Microsoft Teams
- **Questions**: Ask in team chat or during meetings
- **Issues**: Use GitHub Issues for bugs/features

## 🎓 Learning Philosophy

- **Ask Questions**: No question is too basic
- **Document Learnings**: Share what you discover
- **Code Reviews**: Learn from each other's approaches
- **Pair Programming**: Work together on complex features

## 🔐 Security

- **Never commit** `.env` files or secrets
- **Use environment variables** for sensitive data
- **Follow Django security best practices**
- **Review security docs** before implementing auth features

## 📝 Code Style

- **Python**: Follow PEP 8 style guide
- **Django**: Follow Django coding style
- **Comments**: Explain WHY, not WHAT
- **Docstrings**: Document functions and classes

## ❓ Need Help?

- **Documentation**: Check `docs/` folder
- **Architecture**: See `docs/architecture/system-architecture.md`
- **Team**: Reach out to Gerry (project lead)

## 🎵 About Mariachi Todo Terreno

Professional mariachi group led by Gerry Ochoa (trumpet). This website serves both business needs (bookings, promotion) and band management (practice coordination, music library).

---

*Welcome to the team! Let's build something great together.* 🎺
