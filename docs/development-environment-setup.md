# Development Environment Setup Guide
*VS Code + venv + uv Configuration for Python Mariachi Website*

---

## 🎯 **Confirmed Technology Stack**

✅ **IDE**: Visual Studio Code  
✅ **Virtual Environment**: venv (Python built-in)  
✅ **Package Manager**: uv (Rust-based, ultra-fast)  
✅ **Cross-Platform**: Windows PC + macOS support

---

## 🖥️ **Windows PC Setup**

### **Step 1: Python Installation**
```bash
# Download Python 3.11+ from python.org
# Ensure "Add Python to PATH" is checked during installation

# Verify installation
python --version
# Should show Python 3.11+ 
```

### **Step 2: Install uv Package Manager**
```bash
# Install uv using pip (one-time only)
pip install uv

# Verify uv installation
uv --version
# Should show uv version info
```

### **Step 3: VS Code Setup**
1. **Install VS Code** from code.visualstudio.com
2. **Install Python Extension Pack**:
   - Python (Microsoft)
   - Python Debugger
   - Pylance (language support)
   - Python Indent
   - Python Docstring Generator

### **Step 4: Project Environment Setup**
```bash
# Navigate to project directory
cd /path/to/python-mariachi-website

# Create virtual environment using venv
python -m venv mariachi-env

# Activate virtual environment (Windows)
mariachi-env\Scripts\activate

# Verify virtual environment is active
# Prompt should show (mariachi-env)

# Create requirements.txt for project dependencies
touch requirements.txt

# Install dependencies using uv (when we have them)
# uv pip install -r requirements.txt
```

---

## 🍎 **macOS Setup**

### **Step 1: Python Installation**
```bash
# Option 1: Using Homebrew (recommended)
brew install python@3.11

# Option 2: Download from python.org
# Avoid system Python to prevent conflicts

# Verify installation
python3 --version
# Should show Python 3.11+
```

### **Step 2: Install uv Package Manager**
```bash
# Install uv using pip3
pip3 install uv

# Or using Homebrew
brew install uv

# Verify uv installation
uv --version
```

### **Step 3: VS Code Setup**
1. **Install VS Code** from code.visualstudio.com
2. **Install same Python Extension Pack** as Windows
3. **Enable Settings Sync** to maintain consistency between environments

### **Step 4: Project Environment Setup**
```bash
# Navigate to project directory
cd /path/to/python-mariachi-website

# Create virtual environment using venv
python3 -m venv mariachi-env

# Activate virtual environment (macOS)
source mariachi-env/bin/activate

# Verify virtual environment is active
# Prompt should show (mariachi-env)

# Ensure cross-platform compatibility
# Use same requirements.txt as Windows setup
```

---

## ⚙️ **VS Code Configuration**

### **Recommended Settings** (`.vscode/settings.json`)
```json
{
    "python.defaultInterpreterPath": "./mariachi-env/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "files.associations": {
        "*.py": "python"
    },
    "editor.formatOnSave": true,
    "python.analysis.typeCheckingMode": "basic"
}
```

### **Recommended Extensions Beyond Python Pack**
- **GitLens**: Enhanced Git integration
- **Docker**: For containerization (future use)
- **Thunder Client**: API testing (alternative to Postman)
- **Material Icon Theme**: Better file icons
- **Bracket Pair Colorizer**: Code readability

---

## 🚀 **uv Package Manager Benefits**

### **Why uv Over pip?**
- **Speed**: 10-100x faster than pip for package installation
- **Better Dependency Resolution**: More reliable conflict resolution
- **Rust-based**: Modern, memory-safe implementation
- **Drop-in Replacement**: Compatible with pip workflows

### **Common uv Commands**
```bash
# Install packages (replaces pip install)
uv pip install package_name

# Install from requirements.txt
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt

# Create requirements.txt from current environment
uv pip freeze > requirements.txt

# Uninstall packages
uv pip uninstall package_name

# List installed packages
uv pip list
```

---

## 🔧 **Project Structure Setup**

### **Initial Directory Structure**
```
python-mariachi-website/
├── mariachi-env/              # Virtual environment (git ignored)
├── src/                       # Source code (to be created)
├── tests/                     # Test suite (to be created)
├── docs/                      # Documentation (existing)
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── .vscode/                   # VS Code settings
│   └── settings.json
├── .gitignore                 # Git ignore file
└── README.md                  # Project documentation
```

### **Create .gitignore File**
```gitignore
# Virtual Environment
mariachi-env/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/

# IDE
.vscode/settings.json
.idea/

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

---

## ✅ **Environment Verification Checklist**

### **After Setup, Verify:**
- [ ] Python 3.11+ installed and accessible
- [ ] uv package manager installed and working
- [ ] VS Code with Python extensions functional
- [ ] Virtual environment created and can be activated
- [ ] Cross-platform consistency (if using both Windows/macOS)
- [ ] Git repository initialized
- [ ] .gitignore configured properly

### **Test Commands**
```bash
# Activate environment
source mariachi-env/bin/activate  # macOS
# mariachi-env\Scripts\activate    # Windows

# Test Python
python --version

# Test uv
uv --version

# Test pip functionality through uv
uv pip list

# Test VS Code Python integration
code .  # Opens project in VS Code
```

---

## 🎯 **Next Steps After Environment Setup**

1. **Framework Selection**: Continue with Django/Flask/FastAPI research
2. **Database Choice**: PostgreSQL vs MongoDB evaluation
3. **Initial Project**: Create "Hello World" application
4. **Team Synchronization**: Ensure all team members have identical setup

---

## 📚 **Learning Resources**

### **uv Documentation**
- [uv Official Documentation](https://github.com/astral-sh/uv)
- [uv vs pip Performance Comparison](https://github.com/astral-sh/uv#performance)

### **VS Code Python**
- [Python in VS Code Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [Python Extension Features](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

### **Virtual Environments**
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Virtual Environment Best Practices](https://realpython.com/python-virtual-environments-a-primer/)

---

*This standardized environment ensures consistent development experience across team members and platforms.*