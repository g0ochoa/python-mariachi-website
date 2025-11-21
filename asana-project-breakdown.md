# Python Mariachi Website - Task Planning
*Simple task breakdown for Asana project management*

---

## 🎯 **Project Information**
**Project Name**: Python Mariachi Website  
**Team Lead**: Gerry Ochoa  
**Team**: Paco "Sensei" Cisneros, Carlos Cortes, Juan Marin, Gerry Ochoa  
**Start Date**: November 10, 2025  
**Meetings**: Weekly Mondays on Microsoft Teams  
**Project Goal**: Learn Python web development while building mariachi website

---

## 📋 **What This Document Is**

This document helps you understand what tasks to create in Asana. 

**For Asana, we use simple structure:**
- **Work Areas** (Asana Sections) = Epic 1, Epic 2, etc.
- **Tasks** (Asana Tasks) = Individual work items with [E1] [8] format
- **Subtasks** (Asana Subtasks) = Break down complex tasks

**No complex hierarchy needed** - just organized sections and clear tasks!

---

## 🎯 **Sprint 1 Team Assignments** *(Updated After Kickoff - Nov 10, 2025)*

### **Framework Research Task Distribution** *(Updated)*
**New Approach**: Each team member researches ALL 4 frameworks for comprehensive evaluation

- **🥋 Paco "Sensei" Cisneros**: All Frameworks Research (Django, Flask, FastAPI, Streamlit)
- **💻 Carlos Cortes**: All Frameworks Research (Django, Flask, FastAPI, Streamlit)  
- **🎯 Gerry Ochoa**: All Frameworks Research (Django, Flask, FastAPI, Streamlit) + Decision Matrix (Task 1.1.5)
- **🌱 Juan Marin**: All Frameworks Research (Django, Flask, FastAPI, Streamlit) + **Website Design & Mockup** (NEW)

**Deadline**: November 17, 2025 (Monday meeting)  
**Deliverable**: Each member presents comprehensive framework analysis + Juan presents design mockup  
**Decision**: Framework selection finalized by November 20, 2025

### **Additional Task - Website Design** *(NEW)*
- **🌱 Juan Marin**: Website Design Research & Mockup Creation
  - Research modern mariachi website designs
  - Create visual mockup for public website and musicians portal
  - Present design recommendations at November 17 meeting

### **Current Status** *(November 13, 2025)*
- **Days until presentations**: 4 days (presentations on November 17)
- **Research progress**: In progress by all team members
- **GitHub research files**: Available in `docs/framework-research/` directory
- **Next milestone**: Monday, November 17 - Team presentations and discussion

---

## �📊 **Epic Overview & Timeline**

| Epic | Priority | Estimated Duration | Dependencies |
|------|----------|-------------------|--------------|
| **Epic 1**: Technology Stack & Architecture | 🔴 Critical | 1-2 weeks | None |
| **Epic 2**: Development Environment Setup | 🔴 Critical | 1 week | Epic 1 |
| **Epic 3**: Project Foundation & Infrastructure | 🟡 High | 2-3 weeks | Epic 2 |
| **Epic 4**: Authentication & Security Framework | 🟡 High | 2-3 weeks | Epic 3 |
| **Epic 5**: Public Website Development | 🟢 Medium | 3-4 weeks | Epic 4 |
| **Epic 6**: Musicians Portal Development | 🟢 Medium | 4-5 weeks | Epic 5 |
| **Epic 7**: Advanced Features & Integration | 🟡 High | 3-4 weeks | Epic 6 |
| **Epic 8**: Infrastructure as Code & Deployment | 🟡 High | 3-4 weeks | Epic 7 |
| **Epic 9**: CI/CD Pipeline & Production | 🔴 Critical | 2-3 weeks | Epic 8 |

---

## 🏗️ **Work Area 1: Technology Stack (E1)**

**What to create in Asana**: Go to your "🏗️ Epic 1: Technology Stack (E1)" section and add these tasks:

### **Tasks for Asana**

**[E1] [8] Research Python Web Frameworks (Django, Flask, FastAPI, Streamlit)**
- **Assign to**: Each team member gets their own copy (Asana creates duplicates)
- **Due date**: November 17, 2025
- **Description**: Research all 4 frameworks for comprehensive comparison. Document pros/cons, security features, learning curve, and Google SSO integration.
- **Subtasks**: 
  - Django framework research
  - Flask framework research  
  - FastAPI framework research
  - Streamlit framework research

**[E1] [5] Create Framework Decision Matrix**
- **Assign to**: Gerry Ochoa
- **Due date**: November 20, 2025  
- **Description**: Compile team research into decision matrix with weighted criteria. Document final framework selection with rationale.
- **Depends on**: Framework research task above

**[E1] [8] Website Design Research and Mockup**
- **Assign to**: Juan Marin
- **Due date**: November 17, 2025
- **Description**: Research mariachi website designs and create mockup for our site. Include both public website and musicians portal designs.
- **Subtasks**:
  - Research 5-10 professional mariachi websites
  - Create mockups for main pages (home, about, gallery, contact)
  - Design musicians portal layout
  - Prepare design presentation for team meeting

**[E1] [3] Database Technology Selection**
- **Assign to**: Carlos Cortes
- **Due date**: November 20, 2025
- **Description**: Research and recommend database technology (PostgreSQL vs MongoDB) based on project needs.
- **Subtasks**:
  - Analyze PostgreSQL for structured data needs
  - Evaluate MongoDB for flexible schema requirements
  - Create database selection recommendation

**[E1] [5] Authentication Strategy Planning**
- **Assign to**: Paco Cisneros
- **Due date**: Sprint 2
- **Description**: Research and plan Google Workspace SSO integration for musician authentication
- **Subtasks**:
  - Research Google OAuth 2.0 implementation
  - Plan role-based access control
  - Document MFA integration approach

---

## ⚙️ **Work Area 2: Development Environment (E2)**

**What to create in Asana**: Go to your "⚙️ Epic 2: Environment Setup (E2)" section and add these tasks:

### **Tasks for Asana**

**[E2] [3] Set Up Development Environment**
- **Assign to**: Each team member (individual setup)
- **Due date**: Sprint 2 Week 1
- **Description**: Configure Python development environment with standardized tools
- **Subtasks**:
  - Install Python 3.11+ 
  - Install uv package manager
  - Configure VS Code with Python extensions
  - Create virtual environment

**[E2] [5] Database Development Setup**
- **Assign to**: Carlos Cortes
- **Due date**: Sprint 2 Week 1
- **Description**: Set up local database for development based on framework decision
- **Subtasks**:
  - Install chosen database (PostgreSQL/MongoDB)
  - Configure database GUI tools
  - Create sample data setup scripts

**[E2] [2] Git Workflow Setup**
- **Assign to**: Gerry Ochoa
- **Due date**: Sprint 2 Week 1
- **Description**: Establish team Git workflow and repository structure
- **Subtasks**:
  - Document Git workflow for team
  - Set up branch protection rules
  - Create issue templates

---

## 🏠 **Work Area 3: Project Foundation (E3)**

**What to create in Asana**: Go to your "🏠 Epic 3: Project Foundation (E3)" section and add these tasks:

### **Tasks for Asana**

**[E3] [8] Initialize Framework Project**
- **Assign to**: Gerry Ochoa
- **Due date**: Sprint 2 Week 2
- **Description**: Initialize project with chosen framework and basic structure
- **Subtasks**:
  - Create project structure following framework best practices
  - Set up configuration files (settings, requirements)
  - Create basic hello world application
  - Get development server running

**[E3] [5] Database Integration**
- **Assign to**: Carlos Cortes
- **Due date**: Sprint 2 Week 2
- **Description**: Connect database and create initial models
- **Subtasks**:
  - Establish database connection
  - Create User model with basic fields
  - Set up migration system
  - Test basic CRUD operations

**[E3] [3] Configuration Management**
- **Assign to**: Paco Cisneros
- **Due date**: Sprint 2 Week 2
- **Description**: Set up environment-specific configurations
- **Subtasks**:
  - Create dev/staging/production configs
  - Implement environment variable management
  - Set up secret management approach

---

## 📝 **Next Steps for Sprint 2**

### **Immediate Tasks (Sprint 1 End - November 20, 2025)**
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

1. **Today (Sprint 1 End)**: Make framework decision using team research
2. **Create Sprint 2 tasks**: Add Work Area 2 & 3 tasks to your Asana project
3. **Assign team members**: Use the suggested assignments above
4. **Future sprints**: Reference Work Areas 4-8 when ready to plan ahead

**Remember**: This is a guide for creating Asana tasks - copy the [E#] [Points] task names exactly into Asana!