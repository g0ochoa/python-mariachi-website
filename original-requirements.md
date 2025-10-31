# Python Mariachi Website - Original Requirements
*Learning-Focused Full-Stack Python Development Project*

---

## 🎯 **Project Purpose & Goals**

### **Primary Objective**
Develop a real-world mariachi band website using Python to gain hands-on experience with Python web development, while creating a production-ready application for Mariachi Todo Terreno.

### **Learning Outcomes**
- Master Python web development frameworks and best practices
- Implement enterprise-grade security patterns and authentication
- Practice Infrastructure as Code (IaC) with Terraform
- Apply CI/CD methodologies in a real project
- Collaborate using Agile project management principles

---

## 🏗️ **Technical Architecture & Stack**

### **Core Technology**
- **Backend Framework**: Python (Django/Flask/FastAPI - to be determined based on learning objectives)
- **Frontend**: Modern web technologies integrated with Python backend
- **Database**: PostgreSQL or MongoDB (to be determined)
- **Infrastructure**: Google Cloud Platform for production deployment

### **Development & Deployment Environments**
1. **Local Development**: 
   - Windows PC and macOS environments
   - Cross-platform compatibility required
   
2. **Staging Environment**: 
   - Ubuntu Server for testing and integration
   - Mirror production configuration
   
3. **Production Environment**: 
   - Google Cloud Platform
   - Scalable, secure, and monitored deployment

### **Infrastructure as Code**
- **Terraform**: Manage all cloud infrastructure
- **Version Control**: GitHub repository for code management
- **CI/CD Pipeline**: Automated testing, building, and deployment

---

## 🌐 **Website Functionality Requirements**

### **Public Website Features**
The customer-facing side accessible to fans, potential clients, and general visitors:

- **Video Gallery**: Professional showcase of performances and promotional content
- **Event Calendar**: Public calendar displaying upcoming performances and availability
- **Event Request System**: Customer portal for submitting booking requests and inquiries
- **About Page**: Band philosophy, beliefs, mission statement, and member profiles
- **Contact Information**: Professional contact details and booking information
- **Responsive Design**: Mobile-first approach for all devices

### **Musicians Portal (Private)**
Secure, authenticated area exclusively for band members:

- **Digital Scores Library**: Complete collection of sheet music and arrangements
- **Advanced Search**: Filter and search capabilities for music catalog
- **Practice Organization**: Tools for scheduling rehearsals and managing practice sessions
- **Professional Score Display**: Clean, organized, printable sheet music presentation
- **Member Dashboard**: Personalized access to relevant band information

---

## 🔐 **Security & Authentication Requirements**

### **Security Principles** *(Based on Security Engineering Expertise Since 2018)*
- **Zero Trust Architecture**: Assume no implicit trust, verify everything
- **Least Privilege Principle**: Minimum necessary access for all users and systems
- **Defense in Depth**: Multiple layers of security controls
- **Secure by Design**: Security considerations integrated from the beginning

### **Authentication & Authorization**
- **Single Sign-On (SSO)**: Google Workspace integration preferred
- **Organization Membership**: Musicians must be verified members of Mariachi Todo Terreno organization
- **Role-Based Access Control**: Different permission levels for different user types
- **Session Management**: Secure session handling and timeout policies
- **Multi-Factor Authentication**: Additional security layer for sensitive operations

---

## 📊 **Project Management & Collaboration**

### **Team Structure**
- **Project Manager**: Gerry Ochoa (trumpet player, security engineer)
- **Development Team**: Collaborative learning group of friends
- **Methodology**: Agile development with iterative approach

### **Project Management Tools**
- **Asana**: Task assignment, sprint planning, and progress tracking
- **GitHub**: Code repository, issue tracking, and collaboration
- **Documentation**: Comprehensive session logs and learning materials

### **Agile Implementation**
- **Sprint-Based Development**: Regular iterations with defined goals
- **Task Breakdown**: Epics → Stories → Tasks with time estimates
- **Regular Reviews**: Sprint retrospectives and planning sessions
- **Continuous Integration**: Automated testing and quality checks

---

## 📁 **Project Organization & File Structure Requirements**

### **Clean Directory Structure**
- **No Scattered Session Files**: Avoid creating multiple individual session log files
- **Centralized Documentation**: Maintain organized documentation in dedicated directories
- **Logical File Grouping**: Group related files together in meaningful folder structures
- **Consistent Naming Conventions**: Use clear, standardized naming patterns

### **Documentation Organization Standards**
- **Single Master Log**: Maintain one comprehensive development log instead of multiple session files
- **Structured Documentation**: Organize docs by category (architecture, deployment, security, etc.)
- **Version-Controlled Documentation**: All documentation should be tracked in version control
- **Clean Repository**: Keep root directory uncluttered with proper folder hierarchy

### **Recommended Project Structure**
```
python-mariachi-website/
├── README.md
├── original-requirements.md
├── docs/
│   ├── architecture/
│   ├── deployment/
│   ├── security/
│   └── development-log.md
├── src/
│   ├── backend/
│   ├── frontend/
│   └── shared/
├── infrastructure/
│   └── terraform/
├── tests/
├── scripts/
└── .github/
    └── workflows/
```

---

## 📚 **Documentation & Learning Requirements**

### **Session Documentation Standards**
- **Consolidated Development Log**: Single, well-organized log file for all development activities
- **Command Documentation**: All terminal commands and configurations recorded in context
- **Code Explanations**: Detailed breakdown of implementation decisions within relevant documentation sections
- **Learning Reflections**: Self-assessment questions and concept reviews integrated into development log

### **Knowledge Base Structure**
- **Architectural Documentation**: Design decisions and system architecture explanations
- **Deployment Guides**: Step-by-step deployment and infrastructure setup
- **Security Documentation**: Security implementations and best practices applied
- **Development Notes**: Implementation details and troubleshooting information

### **Educational Components**
- **Concept Explanations**: Why certain approaches were chosen
- **Alternative Solutions**: Discussion of different implementation options
- **Learning Checkpoints**: Regular assessment of understanding
- **Reference Materials**: Links to additional learning resources

---

## 🚀 **Development Approach**

### **Incremental Development**
- **Gradual Feature Implementation**: Build functionality step by step
- **Regular Testing**: Continuous validation of features
- **Documentation-Driven**: Document before, during, and after implementation
- **Learning-Focused**: Prioritize understanding over speed

### **Quality Assurance**
- **Code Reviews**: Peer review process for all changes
- **Security Audits**: Regular security assessments and penetration testing
- **Performance Testing**: Load testing and optimization
- **User Acceptance Testing**: Validation with actual band members

---

## 📋 **Success Criteria**

### **Technical Objectives**
- [ ] Fully functional Python-based website deployed to production
- [ ] Secure authentication system integrated with Google Workspace
- [ ] Complete digital scores library with search functionality
- [ ] Automated CI/CD pipeline with Terraform infrastructure
- [ ] Comprehensive documentation and learning materials

### **Learning Objectives**
- [ ] Team proficiency in Python web development
- [ ] Understanding of enterprise security practices
- [ ] Experience with Infrastructure as Code (Terraform)
- [ ] Practical knowledge of Agile project management
- [ ] Real-world application of CI/CD principles

### **Business Objectives**
- [ ] Professional website enhancing Mariachi Todo Terreno's online presence
- [ ] Efficient practice organization tools for band members
- [ ] Streamlined customer interaction and booking system
- [ ] Scalable platform for future enhancements

---

## 🎵 **Domain Context**
**Mariachi Todo Terreno** is a professional mariachi group led by Gerry Ochoa (trumpet). The website serves dual purposes: promoting the band's services to potential clients and providing practical tools for band management and practice coordination.

---

*This document serves as the foundational requirements for the Python Mariachi Website project and should be referenced throughout development to ensure all objectives are met.*