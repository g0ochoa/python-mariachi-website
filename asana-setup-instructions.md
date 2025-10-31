# Asana Project Setup Instructions
*Step-by-Step Guide for Python Mariachi Website Project*

---

## 🎯 **Pre-Setup Preparation**

### **Information You'll Need**
- **Project Name**: `Python Mariachi Website`
- **Team Members**: Your learning group friends (add emails as you get them)
- **Project Timeline**: Start Date: October 29, 2025
- **Sprint Duration**: 2 weeks per sprint

---

## 📋 **Step 1: Create New Project**

### **1.1 Project Creation**
1. **Log into Asana** and go to your workspace
2. **Click "+" button** → "Project"
3. **Choose "Blank Project"** (we'll customize it)
4. **Project Name**: `Python Mariachi Website`
5. **Project Description**: 
   ```
   Learning-focused Python web development project for Mariachi Todo Terreno. 
   Building professional website with public content and private musicians portal.
   Focus: Python frameworks, security engineering, Infrastructure as Code, CI/CD.
   ```

### **1.2 Project Settings**
- **Privacy**: Set to your preference (Private if sensitive, Team if collaborative)
- **Project Color**: Choose a color (suggest blue/green for tech projects)
- **Project Layout**: Choose "List" view (easier for task management)

---

## 📊 **Step 2: Create Custom Fields** *(Recommended)*

### **2.1 Add Custom Fields for Better Tracking**
Go to **Project Settings** → **Custom Fields** → **Add Field**

**Create These Fields**:

1. **Epic** (Dropdown)
   - Epic 1: Technology Stack & Architecture
   - Epic 2: Development Environment Setup
   - Epic 3: Project Foundation & Infrastructure
   - Epic 4: Authentication & Security Framework
   - Epic 5: Public Website Development
   - Epic 6: Musicians Portal Development
   - Epic 7: Advanced Features & Integration
   - Epic 8: Infrastructure as Code & Deployment
   - Epic 9: CI/CD Pipeline & Production

2. **Story Points** (Number)
   - For effort estimation (1, 2, 3, 5, 8, 13, 21)

3. **Sprint** (Dropdown)
   - Sprint 1: Foundation & Decisions (Weeks 1-2)
   - Sprint 2: Project Foundation (Weeks 3-4)
   - Sprint 3: Security Framework (Weeks 5-6)
   - Sprint 4: Public Website (Weeks 7-8)
   - Sprint 5: Musicians Portal (Weeks 9-10)
   - Sprint 6: Advanced Features (Weeks 11-12)
   - Sprint 7: Infrastructure (Weeks 13-14)
   - Sprint 8: Production Deploy (Weeks 15-16)

4. **Learning Focus** (Multi-select)
   - Python Framework
   - Database Design
   - Security Implementation
   - Authentication/SSO
   - Infrastructure/DevOps
   - CI/CD Pipeline
   - Documentation

---

## 🏗️ **Step 3: Create Project Structure**

### **3.1 Create Main Sections** *(Use Asana Sections)*

**Create these sections in order**:
1. **📋 PROJECT PLANNING & DECISIONS**
2. **🚀 SPRINT 1: FOUNDATION & DECISIONS (Weeks 1-2)**
3. **🔧 SPRINT 2: PROJECT FOUNDATION (Weeks 3-4)**
4. **🛡️ SPRINT 3: SECURITY FRAMEWORK (Weeks 5-6)**
5. **🌐 SPRINT 4: PUBLIC WEBSITE (Weeks 7-8)**
6. **🎵 SPRINT 5: MUSICIANS PORTAL (Weeks 9-10)**
7. **⚡ SPRINT 6: ADVANCED FEATURES (Weeks 11-12)**
8. **☁️ SPRINT 7: INFRASTRUCTURE (Weeks 13-14)**
9. **🚀 SPRINT 8: PRODUCTION DEPLOY (Weeks 15-16)**
10. **✅ COMPLETED TASKS**
11. **📚 DOCUMENTATION & LEARNING**

---

## 📝 **Step 4: Create Epic 1 Tasks** *(Start Here)*

### **4.1 Add Tasks to "SPRINT 1" Section**

**Create these tasks in order** *(Copy task names exactly)*:

#### **Story 1.1: Python Web Framework Selection**

**Task 1**: `Research Django Framework`
- **Assignee**: Gerry Ochoa
- **Due Date**: November 5, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 3
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Python Framework
- **Description**:
  ```
  Comprehensive analysis of Django for mariachi website requirements
  
  Acceptance Criteria:
  - Document Django pros/cons for our use case
  - Evaluate built-in admin, ORM, and authentication features  
  - Assess Google Workspace SSO integration capabilities
  - Review security features and best practices
  
  Research Areas:
  - Built-in security features (CSRF, XSS protection, etc.)
  - Authentication system flexibility
  - Admin interface capabilities for content management
  - Learning resources and documentation quality
  - Deployment options and scalability
  ```

**Task 2**: `Research Flask Framework`
- **Assignee**: [Team Member Name]
- **Due Date**: November 5, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 3
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Python Framework
- **Description**:
  ```
  Analysis of Flask for lightweight, custom implementation approach
  
  Acceptance Criteria:
  - Document Flask flexibility and learning benefits
  - Evaluate extension ecosystem (Flask-Login, Flask-SQLAlchemy, etc.)
  - Assess security implementation requirements
  - Review deployment and scaling considerations
  
  Research Areas:
  - Extension ecosystem maturity and security
  - Custom authentication implementation complexity
  - Learning curve for team members
  - Performance characteristics
  - Google Cloud deployment options
  ```

**Task 3**: `Research FastAPI Framework`
- **Assignee**: [Team Member Name]
- **Due Date**: November 5, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 3
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Python Framework
- **Description**:
  ```
  Modern API framework evaluation for performance and features
  
  Acceptance Criteria:
  - Document FastAPI performance and async capabilities
  - Evaluate automatic API documentation features
  - Assess authentication and security implementations
  - Review learning curve and documentation quality
  
  Research Areas:
  - Async/await performance benefits
  - Automatic OpenAPI documentation generation
  - OAuth2/SSO integration patterns
  - Type hints and modern Python features
  - Production deployment considerations
  ```

**Task 4**: `Research Streamlit Framework`
- **Assignee**: [Team Member Name]
- **Due Date**: November 5, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 3
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Python Framework
- **Description**:
  ```
  Rapid web app development framework evaluation for data-driven applications
  
  Acceptance Criteria:
  - Document Streamlit's rapid development capabilities
  - Evaluate suitability for mariachi website requirements
  - Assess authentication options and multi-page applications
  - Review deployment options and production readiness
  - Analyze pros/cons for public website vs data dashboard use cases
  
  Research Areas:
  - Multi-page application capabilities
  - Custom CSS/styling flexibility for professional websites
  - Authentication integration (especially Google SSO)
  - File upload/management for scores library
  - Performance with media content (videos/images)
  - Production deployment and scaling options
  - Community ecosystem and third-party components
  ```

**Task 5**: `Framework Decision Matrix & Selection`
- **Assignee**: Gerry Ochoa (Project Manager)
- **Due Date**: November 7, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 2
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Python Framework
- **Dependencies**: Tasks 1, 2, 3
- **Description**:
  ```
  Create decision matrix and select optimal framework
  
  Acceptance Criteria:
  - Complete comparison matrix with weighted criteria
  - Consider learning objectives, security requirements, and scalability
  - Document final framework selection with rationale
  - Team consensus on chosen framework
  
  Decision Criteria:
  - Learning value for team (40%)
  - Security features and implementation ease (25%)
  - Google Workspace SSO integration (15%)
  - Documentation and community support (10%)
  - Deployment and scaling capabilities (10%)
  ```

#### **Story 1.2: Database Technology Selection**

**Task 6**: `PostgreSQL Analysis for Mariachi Website`
- **Assignee**: [Team Member Name]
- **Due Date**: November 8, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 2
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Database Design
- **Description**:
  ```
  Evaluate PostgreSQL for relational data needs
  
  Acceptance Criteria:
  - Assess PostgreSQL for user management and authentication
  - Evaluate for structured data (scores, events, user profiles)
  - Review Google Cloud PostgreSQL integration
  - Document backup and scaling considerations
  ```

**Task 7**: `MongoDB Analysis for Flexible Schema`
- **Assignee**: [Team Member Name]
- **Due Date**: November 8, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 2
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Database Design
- **Description**:
  ```
  Evaluate MongoDB for document-based approach
  
  Acceptance Criteria:
  - Assess MongoDB for flexible score metadata storage
  - Evaluate for user-generated content and file references
  - Review Google Cloud MongoDB options
  - Document performance implications
  ```

**Task 8**: `Database Architecture Decision`
- **Assignee**: Gerry Ochoa
- **Due Date**: November 10, 2025
- **Epic**: Technology Stack & Architecture
- **Story Points**: 1
- **Sprint**: Sprint 1: Foundation & Decisions
- **Learning Focus**: Database Design
- **Dependencies**: Tasks 6, 7
- **Description**:
  ```
  Select database technology with architectural justification
  
  Acceptance Criteria:
  - Final database selection with detailed rationale
  - Database schema design approach documented
  - Integration plan with chosen web framework
  - Migration and backup strategy outlined
  ```

---

## 🔗 **Step 5: Set Up Dependencies**

### **5.1 Link Task Dependencies**
For each task with dependencies:
1. **Open the dependent task**
2. **Click "Add Dependencies"**
3. **Select the prerequisite tasks**
4. **This will automatically adjust due dates**

**Example**: Task 4 (Framework Decision) depends on Tasks 1, 2, 3

---

## 📊 **Step 6: Create Project Dashboard**

### **6.1 Add Project Dashboard Views**
1. **Go to "Dashboard" tab** in your project
2. **Add these charts**:
   - **Tasks by Sprint** (Donut chart)
   - **Tasks by Epic** (Bar chart)
   - **Completion over time** (Burndown chart)
   - **Tasks by Learning Focus** (Donut chart)

---

## 👥 **Step 7: Team Setup & Invitations**

### **7.1 Invite Team Members**
1. **Click "Share" button** in project header
2. **Add team member emails**
3. **Set permissions** (Editor for active developers)
4. **Send invitations** with welcome message

### **7.2 Welcome Message Template**
```
Welcome to the Python Mariachi Website project! 

This is our learning-focused development project for Mariachi Todo Terreno. 
Please review the original-requirements.md and asana-project-breakdown.md 
files in our GitHub repo for complete project context.

We're following Agile methodology with 2-week sprints. Sprint 1 focuses 
on critical technology decisions - framework and database selection.

Looking forward to collaborating and learning together!
```

---

## ⚙️ **Step 8: Project Automation** *(Optional but Recommended)*

### **8.1 Set Up Rules** *(If you have Asana Premium)*
1. **Go to Project Settings** → **Rules**
2. **Create rule**: "When task is completed" → "Move to Completed Tasks section"
3. **Create rule**: "When task due date passes" → "Add comment requesting status update"

---

## 📋 **Step 9: Initial Sprint Planning**

### **9.1 Set Sprint 1 Goals**
**Add this as the first task** in Sprint 1 section:

**Task**: `Sprint 1 Planning & Goals`
- **Assignee**: Gerry Ochoa
- **Due Date**: October 29, 2025 (Today)
- **Epic**: Technology Stack & Architecture
- **Description**:
  ```
  Sprint 1 Objectives (2 weeks):
  - Complete framework research and selection (Django/Flask/FastAPI)
  - Complete database research and selection (PostgreSQL/MongoDB)
  - Begin development environment setup with confirmed tooling
  - Document all technology decisions with detailed rationale
  
  ✅ CONFIRMED DECISIONS:
  - IDE: Visual Studio Code
  - Virtual Environment: venv 
  - Package Manager: uv (ultra-fast Python package installer)
  
  Success Criteria:
  - Framework decision documented with team consensus
  - Database choice finalized with architecture plan
  - Development environment setup initiated with confirmed tools
  - Sprint 2 planning completed
  ```

---

## 🎯 **Step 10: Next Steps After Asana Setup**

### **10.1 Immediate Actions**
1. **Assign remaining tasks** to team members
2. **Schedule Sprint 1 kickoff meeting**
3. **Create shared research templates**
4. **Set up regular check-in schedule**

### **10.2 Research Templates to Create**
I can help you create standardized research templates for:
- Framework evaluation criteria
- Database assessment framework  
- Security analysis checklist
- Decision documentation format

---

## ✅ **Verification Checklist**

Before starting Sprint 1, verify:
- [ ] All Epic 1 tasks created and assigned
- [ ] Custom fields configured and applied
- [ ] Team members invited and onboarded
- [ ] Dependencies set between tasks
- [ ] Due dates realistic and achievable
- [ ] Project dashboard configured
- [ ] First sprint meeting scheduled

---

**🚀 Ready to begin Sprint 1! The critical technology decisions will set the foundation for your entire Python learning journey.**