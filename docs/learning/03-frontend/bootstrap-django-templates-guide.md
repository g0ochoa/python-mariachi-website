# Bootstrap 5 & Django Templates - Complete Guide
*Building Responsive Web Interfaces for the Mariachi Website*

---

## 🎯 Learning Objectives

By the end of this guide, you will understand:
1. What Bootstrap is and why we use it
2. How to integrate Bootstrap with Django
3. Django template inheritance and reusable layouts
4. Bootstrap grid system for responsive design
5. Common Bootstrap components
6. Custom styling with CSS
7. Best practices for maintainable templates

---

## 📚 Table of Contents

1. [Introduction to Bootstrap](#introduction-to-bootstrap)
2. [Setting Up Bootstrap in Django](#setting-up-bootstrap-in-django)
3. [Django Template System](#django-template-system)
4. [Bootstrap Grid System](#bootstrap-grid-system)
5. [Bootstrap Components](#bootstrap-components)
6. [Custom Styling](#custom-styling)
7. [Responsive Design](#responsive-design)
8. [JavaScript Integration](#javascript-integration)
9. [Best Practices](#best-practices)
10. [Practice Exercises](#practice-exercises)

---

## Introduction to Bootstrap

### What is Bootstrap?

**Bootstrap** is a free, open-source CSS framework developed by Twitter. It provides pre-built components and a responsive grid system to quickly build professional-looking websites.

### Why Use Bootstrap?

**Advantages**:
- ✅ **Speed**: Build interfaces 10x faster than writing custom CSS
- ✅ **Responsive**: Mobile-first design built-in
- ✅ **Consistent**: Looks professional across all browsers
- ✅ **Components**: Pre-built buttons, forms, navbars, etc.
- ✅ **Documentation**: Excellent docs and large community
- ✅ **Learning**: Easy for team members to learn

**When NOT to Use**:
- ❌ Need unique, highly custom design
- ❌ Want minimal CSS (Bootstrap is large)
- ❌ Building simple landing page (might be overkill)

### Bootstrap Alternatives

| Framework | Best For | Learning Curve |
|-----------|----------|----------------|
| **Tailwind CSS** | Utility-first approach, full customization | Steep |
| **Bulma** | Flexbox-based, lightweight | Moderate |
| **Foundation** | Enterprise apps | Moderate |
| **Pure CSS** | Minimal framework | Easy |

**Our Choice**: Bootstrap - Best balance for team learning

---

## Setting Up Bootstrap in Django

### Method 1: CDN (Content Delivery Network)

**What We Used**: This is the simplest method.

**In `templates/base.html`**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Site{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css">
</head>
<body>
    {% block content %}{% endblock %}
    
    <!-- Bootstrap JavaScript -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Advantages**:
- ✅ No download needed
- ✅ Fast (cached globally)
- ✅ Always up-to-date
- ✅ Simple setup

**Disadvantages**:
- ❌ Requires internet connection
- ❌ Less control over version
- ❌ External dependency

### Method 2: Local Files (Alternative)

**Download Bootstrap**:
1. Download from https://getbootstrap.com/docs/5.3/getting-started/download/
2. Extract to `static/bootstrap/`
3. Reference in templates:

```html
{% load static %}
<link href="{% static 'bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">
<script src="{% static 'bootstrap/js/bootstrap.bundle.min.js' %}"></script>
```

**When to Use**: Production environments, no internet dependency needed

### Method 3: Package Manager (Advanced)

**Using npm** (if you have Node.js):
```bash
npm install bootstrap
```

**When to Use**: When using build tools (Webpack, Vite), customizing Bootstrap SASS

---

## Django Template System

### Template Inheritance

**Concept**: Create a base template, then extend it for specific pages.

**Benefits**:
- 🎯 Write navigation once, use everywhere
- 🎯 Consistent design across site
- 🎯 Easy to maintain and update
- 🎯 DRY (Don't Repeat Yourself) principle

### Base Template Structure

**File**: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Default Title{% endblock %}</title>
    
    <!-- CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation (same on all pages) -->
    <nav class="navbar">
        <a href="{% url 'home' %}">Home</a>
    </nav>
    
    <!-- Content (different on each page) -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer (same on all pages) -->
    <footer>
        <p>&copy; 2026 My Site</p>
    </footer>
    
    <!-- JavaScript -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template

**File**: `public_site/templates/public_site/home.html`

```html
{% extends 'base.html' %}

{% block title %}Home - My Site{% endblock %}

{% block content %}
    <h1>Welcome to My Site!</h1>
    <p>This is the home page content.</p>
{% endblock %}

{% block extra_js %}
    <script>
        console.log('Home page loaded');
    </script>
{% endblock %}
```

**How It Works**:
1. `{% extends 'base.html' %}` - Inherit from base
2. `{% block name %}...{% endblock %}` - Fill in blocks
3. Blocks not filled use base template's default

### Template Tags Reference

| Tag | Purpose | Example |
|-----|---------|---------|
| `{% extends %}` | Inherit from parent template | `{% extends 'base.html' %}` |
| `{% block %}` | Define/override content areas | `{% block content %}...{% endblock %}` |
| `{% include %}` | Include another template | `{% include 'partials/navbar.html' %}` |
| `{% load %}` | Load template tag library | `{% load static %}` |
| `{% url %}` | Generate URL from name | `{% url 'home' %}` |
| `{% static %}` | Link to static file | `{% static 'css/style.css' %}` |
| `{% if %}` | Conditional logic | `{% if user.is_authenticated %}...{% endif %}` |
| `{% for %}` | Loop through items | `{% for item in items %}...{% endfor %}` |

### Template Variables

**In View** (`views.py`):
```python
def home(request):
    context = {
        'name': 'John',
        'age': 25,
        'items': ['item1', 'item2', 'item3']
    }
    return render(request, 'home.html', context)
```

**In Template** (`home.html`):
```html
<p>Hello, {{ name }}!</p>
<p>You are {{ age }} years old.</p>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

### Template Filters

**Syntax**: `{{ variable|filter }}`

**Common Filters**:
```html
{{ name|upper }}           <!-- JOHN -->
{{ name|lower }}           <!-- john -->
{{ text|truncatewords:10 }} <!-- First 10 words... -->
{{ date|date:"M d, Y" }}   <!-- Jan 5, 2026 -->
{{ price|floatformat:2 }}  <!-- 19.99 -->
{{ html|safe }}            <!-- Render HTML (use carefully!) -->
```

---

## Bootstrap Grid System

### The 12-Column Grid

Bootstrap divides the page into **12 equal columns**. You can combine columns to create layouts.

**Example**:
```html
<div class="container">
    <div class="row">
        <div class="col-6">6 columns wide (50%)</div>
        <div class="col-6">6 columns wide (50%)</div>
    </div>
    <div class="row">
        <div class="col-4">4 columns (33.33%)</div>
        <div class="col-4">4 columns (33.33%)</div>
        <div class="col-4">4 columns (33.33%)</div>
    </div>
</div>
```

### Responsive Breakpoints

| Class | Screen Size | Device |
|-------|-------------|--------|
| `col-` | < 576px | Extra small (phones portrait) |
| `col-sm-` | ≥ 576px | Small (phones landscape) |
| `col-md-` | ≥ 768px | Medium (tablets) |
| `col-lg-` | ≥ 992px | Large (desktops) |
| `col-xl-` | ≥ 1200px | Extra large (large desktops) |
| `col-xxl-` | ≥ 1400px | XXL (huge screens) |

### Responsive Layout Example

```html
<div class="container">
    <div class="row">
        <!-- Mobile: 100% width, Tablet+: 50% width, Desktop+: 33% width -->
        <div class="col-12 col-md-6 col-lg-4">Column 1</div>
        <div class="col-12 col-md-6 col-lg-4">Column 2</div>
        <div class="col-12 col-md-6 col-lg-4">Column 3</div>
    </div>
</div>
```

**Result**:
- **Mobile** (< 768px): 3 rows, 1 column each (stacked)
- **Tablet** (768-991px): 2 rows, 2 columns in first row, 1 in second
- **Desktop** (992px+): 1 row, 3 columns

### Container Types

```html
<!-- Fixed width, centered -->
<div class="container">...</div>

<!-- Full width (edge to edge) -->
<div class="container-fluid">...</div>

<!-- Responsive: fluid until breakpoint, then fixed -->
<div class="container-md">...</div>
```

---

## Bootstrap Components

### Navigation Bar

**Our Implementation**:
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
    <div class="container">
        <a class="navbar-brand" href="/">
            <i class="bi bi-music-note-beamed"></i>
            Mariachi Todo Terreno
        </a>
        
        <!-- Mobile toggle button -->
        <button class="navbar-toggler" type="button" 
                data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- Navigation links (collapse on mobile) -->
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/about">About</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

**Key Classes**:
- `navbar-expand-lg`: Collapse navigation on screens < 992px
- `navbar-dark bg-dark`: Dark theme
- `sticky-top`: Stay at top when scrolling
- `ms-auto`: Margin-start auto (push to right)

### Buttons

```html
<!-- Colors -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>

<!-- Sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- Outline (not filled) -->
<button class="btn btn-outline-primary">Outline</button>

<!-- Block (full width) -->
<button class="btn btn-primary w-100">Full Width</button>
```

### Cards

```html
<div class="card">
    <img src="image.jpg" class="card-img-top" alt="...">
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Some quick example text.</p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>
```

**Card Variations**:
```html
<!-- With header and footer -->
<div class="card">
    <div class="card-header">Featured</div>
    <div class="card-body">...</div>
    <div class="card-footer text-muted">2 days ago</div>
</div>

<!-- Horizontal card -->
<div class="card mb-3">
    <div class="row g-0">
        <div class="col-md-4">
            <img src="..." class="img-fluid" alt="...">
        </div>
        <div class="col-md-8">
            <div class="card-body">...</div>
        </div>
    </div>
</div>
```

### Forms

```html
<form>
    <!-- Text input -->
    <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input type="text" class="form-control" id="name" required>
        <div class="form-text">Enter your full name</div>
    </div>
    
    <!-- Email input -->
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email">
    </div>
    
    <!-- Select dropdown -->
    <div class="mb-3">
        <label for="event" class="form-label">Event Type</label>
        <select class="form-select" id="event">
            <option value="">Choose...</option>
            <option value="wedding">Wedding</option>
            <option value="party">Party</option>
        </select>
    </div>
    
    <!-- Textarea -->
    <div class="mb-3">
        <label for="message" class="form-label">Message</label>
        <textarea class="form-control" id="message" rows="3"></textarea>
    </div>
    
    <!-- Checkbox -->
    <div class="form-check mb-3">
        <input class="form-check-input" type="checkbox" id="agree">
        <label class="form-check-label" for="agree">
            I agree to terms
        </label>
    </div>
    
    <!-- Submit button -->
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Alerts

```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
{% endif %}
```

**Django Integration**:
```python
from django.contrib import messages

def my_view(request):
    messages.success(request, 'Operation successful!')
    messages.error(request, 'Something went wrong!')
    messages.warning(request, 'Be careful!')
    messages.info(request, 'FYI: something happened')
```

---

## Custom Styling

### CSS Variables

**In `static/css/style.css`**:
```css
:root {
    --primary-color: #8B0000;
    --secondary-color: #FFD700;
    --dark-color: #1A1A1A;
    --light-bg: #F8F9FA;
}

/* Use variables */
.hero {
    background-color: var(--primary-color);
}

button.custom {
    background-color: var(--secondary-color);
}
```

**Benefits**:
- Change colors in one place
- Consistent theming
- Easy to maintain

### Overriding Bootstrap

**Method 1: More Specific Selector**
```css
/* Bootstrap default */
.btn-primary {
    background-color: #0d6efd;
}

/* Your override (more specific) */
.btn.btn-primary {
    background-color: var(--primary-color);
}
```

**Method 2: !important (Last Resort)**
```css
.btn-primary {
    background-color: var(--primary-color) !important;
}
```

**Best Practice**: Use method 1, avoid `!important`

### Custom Component Example

**Our Custom Gold Button**:
```css
.btn-gold {
    background-color: #FFD700;
    border-color: #FFD700;
    color: #1A1A1A;
    font-weight: 600;
}

.btn-gold:hover {
    background-color: #DAA520;
    border-color: #DAA520;
    color: #1A1A1A;
}
```

**Usage**:
```html
<a href="#" class="btn btn-gold btn-lg">Book Now</a>
```

---

## Responsive Design

### Mobile-First Approach

**Bootstrap Philosophy**: Design for mobile first, then enhance for larger screens.

**Example**:
```html
<!-- Default: Full width on mobile -->
<div class="col-12 col-md-6 col-lg-4">
    Content
</div>
```

**Reads as**:
- 12 columns (100%) on mobile
- 6 columns (50%) on tablets+
- 4 columns (33%) on desktops+

### Hiding/Showing Elements

```html
<!-- Hide on small screens -->
<div class="d-none d-md-block">
    Only visible on tablets and up
</div>

<!-- Show only on mobile -->
<div class="d-block d-md-none">
    Only visible on mobile
</div>
```

**Display Utility Classes**:
- `d-none`: Hide
- `d-block`: Show as block
- `d-inline`: Show inline
- `d-flex`: Show as flexbox

### Spacing Utilities

**Format**: `{property}{sides}-{size}` or `{property}{sides}-{breakpoint}-{size}`

**Properties**:
- `m`: margin
- `p`: padding

**Sides**:
- `t`: top
- `b`: bottom
- `s`: start (left)
- `e`: end (right)
- `x`: left and right
- `y`: top and bottom
- blank: all sides

**Sizes**: `0` to `5` (0, 0.25rem, 0.5rem, 1rem, 1.5rem, 3rem)

**Examples**:
```html
<div class="mb-3">Margin bottom 1rem</div>
<div class="px-5">Padding left and right 3rem</div>
<div class="mt-md-4">Margin top 1.5rem on tablets+</div>
```

---

## JavaScript Integration

### Using Bootstrap JavaScript

**Components that Need JavaScript**:
- Dropdowns
- Modals
- Tooltips
- Popovers
- Carousel

**Include Bootstrap Bundle**:
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```

### Example: Modal

```html
<!-- Button trigger -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
    Launch Modal
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Modal Title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Modal body text goes here.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
            </div>
        </div>
    </div>
</div>
```

### Custom JavaScript with Bootstrap

**Our Smooth Scrolling**:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
```

---

## Best Practices

### 1. Template Organization

**Good Structure**:
```
templates/
├── base.html                    # Main base template
├── partials/                    # Reusable components
│   ├── navbar.html
│   ├── footer.html
│   └── messages.html
└── app_name/
    └── page.html                # App-specific pages
```

### 2. Keep Templates Simple

**Bad** (too much logic):
```html
{% if user.is_authenticated and user.role == 'admin' and user.is_active and not user.banned %}
    <!-- Complex nested logic -->
{% endif %}
```

**Good** (logic in view):
```python
# views.py
def my_view(request):
    can_access = (
        request.user.is_authenticated and 
        request.user.role == 'admin' and 
        request.user.is_active and 
        not request.user.banned
    )
    return render(request, 'page.html', {'can_access': can_access})
```

```html
<!-- template -->
{% if can_access %}
    <!-- Clean template -->
{% endif %}
```

### 3. Use Semantic HTML

**Bad**:
```html
<div class="header">
    <div class="navigation">...</div>
</div>
```

**Good**:
```html
<header>
    <nav>...</nav>
</header>
```

### 4. Accessibility

```html
<!-- Always include alt text -->
<img src="photo.jpg" alt="Mariachi band performing">

<!-- Use semantic HTML -->
<button type="button">Click Me</button> <!-- Not <div onclick="..."> -->

<!-- Label form inputs -->
<label for="email">Email</label>
<input type="email" id="email" name="email">

<!-- ARIA labels when needed -->
<button aria-label="Close modal">×</button>
```

### 5. Performance

**Optimize Images**:
```html
<!-- Lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Responsive images -->
<img srcset="image-320w.jpg 320w,
             image-640w.jpg 640w,
             image-1024w.jpg 1024w"
     sizes="(max-width: 640px) 100vw, 50vw"
     src="image-640w.jpg" alt="Description">
```

**Minify Static Files** (Production):
```bash
python manage.py collectstatic --no-input
# Use WhiteNoise or CDN for compression
```

---

## Practice Exercises

### Exercise 1: Create an About Page

**Goal**: Practice template inheritance

**Steps**:
1. Create `public_site/templates/public_site/about.html`
2. Extend `base.html`
3. Add a 2-column layout with image and text
4. Create view and URL for the page

**Hint**:
```html
{% extends 'base.html' %}

{% block content %}
    <div class="container py-5">
        <div class="row">
            <div class="col-md-6">
                <!-- Image -->
            </div>
            <div class="col-md-6">
                <!-- Text -->
            </div>
        </div>
    </div>
{% endblock %}
```

### Exercise 2: Build a Contact Form

**Goal**: Practice Bootstrap forms

**Requirements**:
- Name field
- Email field
- Message textarea
- Submit button
- Form validation (HTML5)

**Challenge**: Make it save to database (needs Django forms)

### Exercise 3: Create a Gallery Grid

**Goal**: Practice grid system

**Requirements**:
- 3 columns on desktop
- 2 columns on tablet
- 1 column on mobile
- Use card components
- Add hover effects

### Exercise 4: Custom Component

**Goal**: Create a reusable component

**Task**: Create a "service card" component
- Icon at top
- Title
- Description
- "Learn More" button
- Hover effect

**Hint**: Use `{% include %}` to make it reusable

---

## Self-Assessment Questions

Test your understanding:

1. **What is the Bootstrap grid system based on?**
   - A) 16 columns
   - B) 12 columns ✓
   - C) 10 columns
   - D) Flexible columns

2. **Which breakpoint is for tablets in Bootstrap?**
   - A) col-sm-
   - B) col-md- ✓
   - C) col-lg-
   - D) col-xl-

3. **What does `{% extends 'base.html' %}` do?**
   - A) Includes another template
   - B) Inherits from base template ✓
   - C) Creates a new template
   - D) Imports CSS

4. **How do you reference static files in Django templates?**
   - A) `{{ static 'file.css' }}`
   - B) `{% static 'file.css' %}` ✓
   - C) `/static/file.css`
   - D) `static('file.css')`

5. **What does `ms-auto` do in Bootstrap?**
   - A) Adds margin on all sides
   - B) Pushes element to the right ✓
   - C) Makes element smaller
   - D) Adds auto margins

**Answers**: 1-B, 2-B, 3-B, 4-B, 5-B

---

## Additional Resources

### Official Documentation
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Django Templates](https://docs.djangoproject.com/en/5.2/topics/templates/)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

### Learning Resources
- [Bootstrap Crash Course](https://www.youtube.com/watch?v=4sosXZsdy-s) (YouTube)
- [Django for Beginners](https://djangoforbeginners.com/)
- [FreeCodeCamp Bootstrap](https://www.freecodecamp.org/news/tag/bootstrap/)

### Tools
- [Bootstrap Builder](https://bootstrap.build/app) - Visual builder
- [BootstrapMade](https://bootstrapmade.com/) - Free templates for inspiration
- [Coolors](https://coolors.co/) - Color palette generator

---

## Summary

**What We Learned**:
- ✅ Bootstrap provides pre-built responsive components
- ✅ Django templates support inheritance for reusable layouts
- ✅ Grid system uses 12 columns with responsive breakpoints
- ✅ CDN is easiest way to include Bootstrap
- ✅ Custom CSS can override and extend Bootstrap
- ✅ Mobile-first approach designs for small screens first
- ✅ Template tags like `{% block %}` and `{% extends %}` create maintainable code

**Next Steps**:
1. Practice building pages with Bootstrap
2. Learn Django forms for functional contact form
3. Study JavaScript for interactive components
4. Explore advanced Bootstrap features (modals, tooltips, etc.)

---

**Guide Version**: 1.0  
**Last Updated**: January 6, 2026  
**Project**: Python Mariachi Website  
**Topic**: Frontend Development
