# Python Mariachi Website - Task Planning
*Simple task breakdown for Asana project management*

---

## 🎯 **Project Information**
**Project Name**: Python Mariachi Website  
**Team Lead**: Gerry Ochoa  
**Team**: Paco "Sensei" Cisneros, Carlos Cortes, Juan Marin, Gerry Ochoa  
**Start Date**: November 24, 2025  
**Meetings**: Weekly Mondays on Microsoft Teams  
**Project Goal**: Learn Python web development while building mariachi website

## 📅 **Sprint Timeline Overview**

### **SPRINT 1: November 24 - December 4, 2025**
- **Focus**: Django project setup and PostgreSQL configuration
- **Work Areas**: Epic 1 (Technology Stack) + Epic 2 (Development Environment) + Epic 3 (Project Foundation)
- **Deliverable**: Working Django project with PostgreSQL database
- **Decisions Made**: Django framework ✅, PostgreSQL database ✅

### **SPRINT 2: December 9 - December 16, 2025**  
- **Focus**: Development environment and project foundation
- **Work Areas**: Epic 2 (Development Environment) + Epic 3 (Project Foundation)
- **Deliverable**: Working "Hello World" application

---

## 📋 **What This Document Is**

This document helps you understand what tasks to create in Asana. 

**For Asana, we use simple structure:**
- **Work Areas** (Asana Sections) = Epic 1, Epic 2, etc.
- **Tasks** (Asana Tasks) = Individual work items with [E1] [8] format
- **Subtasks** (Asana Subtasks) = Break down complex tasks

**No complex hierarchy needed** - just organized sections and clear tasks!

---

## 🎯 **Sprint 1 Team Assignments** *(Starting Nov 24, 2025)*

### **Framework Research Task Distribution** *(Updated)*
**New Approach**: Each team member researches ALL 4 frameworks for comprehensive evaluation

- **🥋 Paco "Sensei" Cisneros**: All Frameworks Research (Django, Flask, FastAPI, Streamlit)
- **💻 Carlos Cortes**: All Frameworks Research (Django, Flask, FastAPI, Streamlit)  
- **🎯 Gerry Ochoa**: All Frameworks Research (Django, Flask, FastAPI, Streamlit) + Decision Matrix (Task 1.1.5)
- **🌱 Juan Marin**: All Frameworks Research (Django, Flask, FastAPI, Streamlit) + **Website Design & Mockup** (NEW)

**Deadline**: December 1, 2025 (Monday meeting)  
**Deliverable**: Each member presents comprehensive framework analysis + Juan presents design mockup  
**Decision**: Framework selection finalized by December 4, 2025

### **Additional Task - Website Design** *(NEW)*
- **🌱 Juan Marin**: Website Design Research & Mockup Creation
  - Research modern mariachi website designs
  - Create visual mockup for public website and musicians portal
  - Present design recommendations at December 1 meeting

### **Current Status** *(November 21, 2025)*
- **Sprint 1 starts**: Monday, November 24, 2025
- **Research progress**: Ready to begin
- **GitHub research files**: Available in `docs/framework-research/` directory
- **Next milestone**: Monday, December 1 - Team presentations and discussion

---

## �📊 **Epic Overview & Timeline**

| Epic | Priority | Estimated Duration | Dependencies | Status |
|------|----------|-------------------|--------------|--------|
| **Epic 1**: Technology Stack & Architecture | 🔴 Critical | 1-2 weeks | None | ✅ COMPLETE |
| **Epic 2**: Development Environment Setup | 🔴 Critical | 1 week | Epic 1 | ✅ COMPLETE |
| **Epic 3**: Project Foundation & Infrastructure | 🟡 High | 2-3 weeks | Epic 2 | ✅ COMPLETE |
| **Epic 3.5**: Frontend Development (Bootstrap) | 🟡 High | 1-2 weeks | Epic 3 | ✅ COMPLETE |
| **Epic 3.6**: Staging Deployment Setup | 🟢 Medium | 1 week | Epic 3.5 | 🔄 IN PROGRESS |
| **Epic 4**: Authentication & Security Framework | 🟡 High | 2-3 weeks | Epic 3 | 🔜 NEXT |
| **Epic 5**: Public Website Development | 🟢 Medium | 3-4 weeks | Epic 4 | Not Started |
| **Epic 6**: Musicians Portal Development | 🟢 Medium | 4-5 weeks | Epic 5 | Not Started |
| **Epic 7**: Advanced Features & Integration | 🟡 High | 3-4 weeks | Epic 6 | Not Started |
| **Epic 8**: Infrastructure as Code & Deployment | 🟡 High | 3-4 weeks | Epic 7 | Not Started |
| **Epic 9**: CI/CD Pipeline & Production | 🔴 Critical | 2-3 weeks | Epic 8 | Not Started |

---

## 🏗️ **Work Area 1: Technology Stack (E1)** - **SPRINT 1**

**What to create in Asana**: Go to your "🏗️ Epic 1: Technology Stack (E1)" section and add these tasks:

### **Tasks for Asana**

**[E1] [8] Research Python Web Frameworks (Django, Flask, FastAPI, Streamlit)** - **SPRINT 1**
- **Assign to**: Each team member gets their own copy (Asana creates duplicates)
- **Due date**: December 1, 2025
- **Description**: Research all 4 frameworks for comprehensive comparison. Document pros/cons, security features, learning curve, and Google SSO integration.
- **Subtasks**: 
  - Django framework research
  - Flask framework research  
  - FastAPI framework research
  - Streamlit framework research

**[E1] [5] Create Framework Decision Matrix** - **SPRINT 1**
- **Assign to**: Gerry Ochoa
- **Due date**: December 4, 2025  
- **Description**: Compile team research into decision matrix with weighted criteria. Document final framework selection with rationale.
- **Depends on**: Framework research task above

**[E1] [8] Website Design Research and Mockup** - **SPRINT 1**
- **Assign to**: Juan Marin
- **Due date**: December 1, 2025
- **Description**: Research mariachi website designs and create mockup for our site. Include both public website and musicians portal designs.
- **Subtasks**:
  - Research 5-10 professional mariachi websites
  - Create mockups for main pages (home, about, gallery, contact)
  - Design musicians portal layout
  - Prepare design presentation for team meeting

**[E1] [3] Database Technology Selection** - **SPRINT 1**
- **Assign to**: Paco Cisneros
- **Due date**: December 4, 2025
- **Description**: Research and recommend database technology (PostgreSQL vs MongoDB) based on project needs.
- **Subtasks**:
  - Analyze PostgreSQL for structured data needs
  - Evaluate MongoDB for flexible schema requirements
  - Create database selection recommendation

**[E1] [5] Authentication Strategy Planning** - **SPRINT 2**
- **Assign to**: Paco Cisneros
- **Due date**: Sprint 2
- **Description**: Research and plan Google Workspace SSO integration for musician authentication
- **Subtasks**:
  - Research Google OAuth 2.0 implementation
  - Plan role-based access control
  - Document MFA integration approach

---
## 🎨 **Work Area 3.5: Frontend Development (E3.5)** - **COMPLETED JAN 5-6, 2026**

**What to create in Asana**: Go to your "🎨 Epic 3.5: Frontend Development (E3.5)" section and add these tasks:

### **Tasks for Asana**

**[E3.5] [5] Bootstrap 5 Integration** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 5, 2026
- **Description**: Integrate Bootstrap 5 CSS framework via CDN for responsive design
- **Subtasks**:
  - Add Bootstrap CSS and JS to base template ✅
  - Include Bootstrap Icons library ✅
  - Add Google Fonts (Playfair Display, Open Sans) ✅
  - Configure static files in Django settings ✅

**[E3.5] [8] Base Template with Navigation** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 5, 2026
- **Description**: Create reusable base template with responsive navigation and footer
- **Subtasks**:
  - Build base.html with template inheritance blocks ✅
  - Implement responsive Bootstrap navbar ✅
  - Add footer with contact info and social links ✅
  - Configure Django messages/alerts display ✅

**[E3.5] [13] Home Page Implementation** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 5, 2026
- **Description**: Build complete home page with all sections using Bootstrap components
- **Deliverables**:
  - Hero section with gradient background ✅
  - About section (2-column layout) ✅
  - Services cards (3 cards with icons) ✅
  - Gallery preview (3-column grid) ✅
  - Events calendar (2 upcoming events) ✅
  - Contact form (non-functional HTML) ✅

**[E3.5] [5] Custom CSS Styling** - **COMPLETED**
- **Assigned to**: Gerry Ochoa (with Juan's design input)
- **Completed**: January 5, 2026
- **Description**: Create custom CSS for mariachi theme and branding
- **Subtasks**:
  - Define CSS variables for color palette ✅
  - Style typography (headers and body) ✅
  - Create custom button styles (btn-gold) ✅
  - Add card hover effects ✅
  - Implement responsive adjustments ✅

**[E3.5] [3] Custom JavaScript** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 5, 2026
- **Description**: Add JavaScript for smooth scrolling and interactivity
- **Subtasks**:
  - Implement smooth scrolling for anchor links ✅
  - Add navbar scroll shadow effect ✅
  - Auto-dismiss alerts after 5 seconds ✅

**[E3.5] [3] URL Routing Configuration** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 5, 2026
- **Description**: Set up URL patterns for public site
- **Subtasks**:
  - Create public_site/urls.py ✅
  - Add home view function ✅
  - Include public_site URLs in project urls.py ✅

---

## 🚀 **Work Area 3.6: Staging Deployment (E3.6)** - **IN PROGRESS JAN 6, 2026**

**What to create in Asana**: Go to your "🚀 Epic 3.6: Staging Deployment (E3.6)" section and add these tasks:

### **Tasks for Asana**

**[E3.6] [5] Production Requirements File** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 6, 2026
- **Description**: Create production-specific requirements.txt with additional packages
- **Subtasks**:
  - Add gunicorn==21.2.0 for WSGI server ✅
  - Add whitenoise==6.6.0 for static file serving ✅
  - Document differences from development requirements ✅

**[E3.6] [8] Deployment Infrastructure Files** - **COMPLETED**
- **Assigned to**: Gerry Ochoa
- **Completed**: January 6, 2026
- **Description**: Create configuration files for Ubuntu staging server deployment
- **Deliverables**:
  - Gunicorn configuration (deployment/gunicorn_config.py) ✅
  - Nginx reverse proxy config (deployment/nginx.conf) ✅
  - Systemd service file (deployment/mariachi-website.service) ✅
  - Automated deployment script (deployment/deploy.sh) ✅

**[E3.6] [8] Deploy to Ubuntu Staging Server** - **IN PROGRESS**
- **Assigned to**: Gerry Ochoa
- **Due date**: January 7, 2026
- **Description**: Execute deployment to Ubuntu server for testing and visual progress tracking
- **Subtasks**:
  - Run deployment script to clone/update repository
  - Set up Python virtual environment on server
  - Install production dependencies
  - Configure environment variables (.env file)
  - Run database migrations
  - Collect static files
  - Configure and start systemd service
  - Configure and restart nginx
  - Test accessibility from network

**[E3.6] [3] Deployment Documentation** - **NOT STARTED**
- **Assigned to**: Gerry Ochoa
- **Due date**: January 8, 2026
- **Description**: Document deployment process and server configuration for team
- **Subtasks**:
  - Document deployment steps
  - Create troubleshooting guide
  - Add server access instructions
  - Document rollback procedure

**[E3.6] [5] Create Deployment Learning Guide** - **NOT STARTED**
- **Assigned to**: Paco Cisneros
- **Due date**: January 10, 2026
- **Description**: Create comprehensive learning guide about manual Linux deployment
- **Topics to cover**:
  - Gunicorn and WSGI servers
  - Nginx reverse proxy concepts
  - Systemd service management
  - Linux file permissions and users
  - Environment variable management
  - Static file serving in production

---
## ⚙️ **Work Area 2: Development Environment (E2)** - **SPRINT 1**

**What to create in Asana**: Go to your "⚙️ Epic 2: Development Environment (E2)" section and add these tasks:

### **Tasks for Asana**

**[E2] [3] Set Up Development Environment** - **SPRINT 2**
- **Assign to**: Each team member (individual setup)
- **Due date**: Sprint 2 Week 1 (December 9, 2025)
- **Description**: Configure Python development environment with standardized tools
- **Subtasks**:
  - Install Python 3.11+ 
  - Install uv package manager
  - Configure VS Code with Python extensions
  - Create virtual environment

**[E2] [5] Database Development Setup** - **SPRINT 2**
- **Assign to**: Carlos Cortes
- **Due date**: Sprint 2 Week 1 (December 9, 2025)
- **Description**: Set up local database for development based on framework decision
- **Subtasks**:
  - Install chosen database (PostgreSQL/MongoDB)
  - Configure database GUI tools
  - Create sample data setup scripts

**[E2] [2] Git Workflow Setup** - **SPRINT 2**
- **Assign to**: Gerry Ochoa
- **Due date**: Sprint 2 Week 1 (December 9, 2025)
- **Description**: Establish team Git workflow and repository structure
- **Subtasks**:
  - Document Git workflow for team
  - Set up branch protection rules
  - Create issue templates

---

## 🏠 **Work Area 3: Project Foundation (E3)** - **SPRINT 2**

**What to create in Asana**: Go to your "🏠 Epic 3: Project Foundation (E3)" section and add these tasks:

### **Tasks for Asana**

**[E3] [8] Initialize Framework Project** - **SPRINT 2**
- **Assign to**: Gerry Ochoa
- **Due date**: Sprint 2 Week 2 (December 16, 2025)
- **Description**: Initialize project with chosen framework and basic structure
- **Subtasks**:
  - Create project structure following framework best practices
  - Set up configuration files (settings, requirements)
  - Create basic hello world application
  - Get development server running

**[E3] [5] Database Integration** - **SPRINT 2**
- **Assign to**: Carlos Cortes
- **Due date**: Sprint 2 Week 2 (December 16, 2025)
- **Description**: Connect database and create initial models
- **Subtasks**:
  - Establish database connection
  - Create User model with basic fields
  - Set up migration system
  - Test basic CRUD operations

**[E3] [3] Configuration Management** - **SPRINT 2**
- **Assign to**: Paco Cisneros
- **Due date**: Sprint 2 Week 2 (December 16, 2025)
- **Description**: Set up environment-specific configurations
- **Subtasks**:
  - Create dev/staging/production configs
  - Implement environment variable management
  - Set up secret management approach

---

## 📝 **Next Steps for Sprint 2**

### **Immediate Tasks (Sprint 1 End - December 4, 2025)**
1. **Complete framework decision** using research findings
2. **Create Sprint 2 tasks** in Asana based on chosen framework
3. **Update team assignments** for Sprint 2 work
4. **Schedule Sprint 2 kickoff** meeting

### **Sprint 2 Focus Areas**
- **Week 1**: Development environment setup for all team members
- **Week 2**: Project initialization and basic structure
- **Goal**: Working "Hello World" application by end of Sprint 2

---

## 📅 **Future Work Areas** *(For Later Sprints)*

### **🔐 Work Area 4: Authentication & Security (E4)**
- Google Workspace SSO implementation
- Role-based access control
- Security framework setup

### **🌐 Work Area 5: Public Website (E5)**
- Home, About, Gallery, Contact pages
- Responsive design implementation
- Content management

### **🎵 Work Area 6: Musicians Portal (E6)**
- Private login area
- Score library
- Practice tools

### **✨ Work Area 7: Advanced Features (E7)**
- File sharing
- Event calendar
- Audio recording tools

### **☁️ Work Area 8: Deployment (E8)**
- Production deployment
- CI/CD pipeline
- Monitoring setup

---

## ✅ **How to Use This Document**

1. **Sprint 1 (Nov 24 - Dec 4)**: Complete framework research and make decision
2. **Create Sprint 2 tasks**: Add Work Area 2 & 3 tasks to your Asana project
3. **Assign team members**: Use the suggested assignments above
4. **Future sprints**: Reference Work Areas 4-8 when ready to plan ahead

**Remember**: This is a guide for creating Asana tasks - copy the [E#] [Points] task names exactly into Asana!