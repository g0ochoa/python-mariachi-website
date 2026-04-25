# Django Models, Forms & The Contact Form — Learning Guide
**Understanding how data flows from an HTML form into your database**

*Author: Gerry Ochoa*  
*Date: April 22, 2026*  
*Sprint: Sprint 3, Phase 1*  
*Purpose: Educational resource — explains what we built, why, and how it works*

---

## 📚 Table of Contents

1. [Big Picture: What We're Building](#big-picture)
2. [Part 1: Models — Your Database Blueprint](#part-1-models)
3. [Part 2: Migrations — Teaching Django About Your Model](#part-2-migrations)
4. [Part 3: Forms — Connecting HTML to Python](#part-3-forms)
5. [Part 4: Views — The Traffic Controller](#part-4-views)
6. [Part 5: Templates — Making It Look Good](#part-5-templates)
7. [Part 6: The Admin Panel — Free Superpower](#part-6-admin)
8. [The Full Request Lifecycle](#full-lifecycle)
9. [Common Mistakes & How to Fix Them](#common-mistakes)
10. [Self-Assessment Questions](#self-assessment)

---

## 🎯 Big Picture: What We're Building {#big-picture}

When a visitor fills out the "Contact Us" form on the home page, we want:

1. Their information to be **saved to a database** (not just emailed and potentially lost)
2. If they fill something in wrong, show them **helpful error messages** (not just reset the form)
3. After a successful submission, show a **confirmation message**
4. Gerry should be able to **log into the admin panel** and see all inquiries

Here's the journey data takes:

```
Visitor fills form → Browser sends POST request
                         ↓
                   Django URL router → home() view
                         ↓
                   ContactForm.is_valid()
                     ↓           ↓
                  Valid        Invalid
                    ↓             ↓
             form.save()    Re-render form
                    ↓        with errors
             redirect('home')
                    ↓
             Flash message: "¡Gracias!"
```

---

## 📦 Part 1: Models — Your Database Blueprint {#part-1-models}

### What is a Model?

A **model** is a Python class that represents a database table. Each attribute of the class becomes a column in the table.

**Without Django**, you'd write raw SQL:
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    ...
);
```

**With Django**, you write Python:
```python
class BookingRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ...
```

Django generates the SQL for you. You never have to write `CREATE TABLE` by hand.

---

### Field Types — Choose the Right Tool

| Field Type | What It Stores | Example Use |
|-----------|---------------|------------|
| `CharField(max_length=N)` | Short text | Name, phone number |
| `EmailField()` | Email address (validates format) | Contact email |
| `TextField()` | Long text (no length limit) | Message body |
| `BooleanField()` | True / False | Opted in to promos? |
| `DateTimeField(auto_now_add=True)` | Date + time, set automatically | When form was submitted |
| `IntegerField()` | Whole number | Age, quantity |
| `ForeignKey()` | Link to another model | Song belongs to a collection |

> **Why `EmailField` instead of `CharField`?**  
> `EmailField` runs validation — Django will reject `"not-an-email"` automatically, before it even reaches your view code.

---

### The `choices` Parameter — Human-Readable Options

```python
EVENT_CHOICES = [
    ('wedding', 'Wedding'),
    ('quinceanera', 'Quinceañera'),
    ...
]
event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
```

Each choice is a **tuple**: `(database_value, display_label)`.

- **In the database**: stored as `"wedding"` (short, no special characters)
- **In the admin/templates**: shown as `"Wedding"` (nice and readable)

To get the human label in Python code:
```python
booking = BookingRequest.objects.get(id=1)
booking.get_event_type_display()  # → "Wedding"
```

---

### The `Meta` Class — Table Configuration

```python
class Meta:
    ordering = ['-submitted_at']  # Newest first (the - means descending)
```

This tells Django: *whenever you query all BookingRequests, sort them newest first by default.*

---

### The `__str__` Method — Human-Readable Representation

```python
def __str__(self):
    return f"{self.name} - {self.get_event_type_display()} ({self.submitted_at.date()})"
```

Without `__str__`, the admin panel shows `BookingRequest object (1)`.  
With it, you see: `"José García - Wedding (2026-04-22)"`.

Always define `__str__` on your models. It's a quality-of-life necessity.

---

## 🔄 Part 2: Migrations — Teaching Django About Your Model {#part-2-migrations}

### The Problem

Your Python class exists — but the *database table* doesn't yet. Django needs to create it.

### The Two-Step Process

**Step 1: Generate the migration file**
```bash
python manage.py makemigrations public_site
```
This creates `public_site/migrations/0001_initial.py` — a Python file that describes what SQL to run.

**Step 2: Actually run the SQL**
```bash
python manage.py migrate
```
This reads all pending migration files and executes the database changes.

### Why Two Steps?

Because migrations are also **version history for your database schema**.

If you're working with a team and a teammate adds a new field, they generate a migration, commit it to Git, and you just run `python manage.py migrate` to catch up. No manual SQL scripts, no "hey what tables do you have?"

### Golden Rule: Never Edit Migration Files

Django auto-generates them. If you edit them by hand, you can corrupt your migration history. If you need to change a field, change the model and run `makemigrations` again.

---

## 📋 Part 3: Forms — Connecting HTML to Python {#part-3-forms}

### Two Types of Django Forms

| Type | Use When |
|------|---------|
| `forms.Form` | The form doesn't map to a database model |
| `forms.ModelForm` | The form creates/updates a database record ← **our case** |

### Why ModelForm?

Compare the manual way vs. ModelForm:

**Manual approach (tedious, error-prone):**
```python
# In your view, after POST:
name = request.POST.get('name')
email = request.POST.get('email')
# ... validate each field yourself ...
# ... check for missing required fields ...
# ... sanitize inputs ...
booking = BookingRequest(name=name, email=email, ...)
booking.save()
```

**ModelForm approach (clean, automatic):**
```python
form = ContactForm(request.POST)
if form.is_valid():   # ← validates everything automatically
    form.save()       # ← saves to database automatically
```

The ModelForm handles validation, sanitization, and database insertion in three lines.

---

### The `Meta` Class Inside a Form

```python
class ContactForm(forms.ModelForm):
    class Meta:
        model = BookingRequest          # Which model to use
        fields = ['name', 'email', ...]  # Which fields to include
        widgets = { ... }               # Customize the HTML input elements
        labels = { ... }                # Customize the field labels
```

The `Meta` class (inner class) is how you configure the ModelForm's behavior.

### Widgets — Customizing HTML Output

A **widget** is the HTML element that represents a field.

```python
widgets = {
    'name': forms.TextInput(attrs={
        'class': 'form-control',      # Bootstrap CSS class
        'placeholder': 'Your full name',
    }),
}
```

Without a custom widget, Django renders `<input type="text" name="name">`.  
With our widget, it renders `<input type="text" name="name" class="form-control" placeholder="Your full name">`.

The `attrs` dict maps directly to HTML attributes.

---

## 🎛️ Part 4: Views — The Traffic Controller {#part-4-views}

### The Post-Redirect-Get (PRG) Pattern

This is one of the most important web development patterns. Here's why it matters:

**Without PRG — the problem:**
```
1. User fills form and clicks Submit
2. Browser sends POST to /
3. Django saves data and renders "Thank you" page
4. User presses F5 (refresh)
5. Browser says "Resend form data?" — user clicks OK
6. Form is submitted AGAIN → duplicate record in database
```

**With PRG — the solution:**
```
1. User fills form and clicks Submit  
2. Browser sends POST to /
3. Django saves data, then sends 302 Redirect to /
4. Browser follows redirect — sends GET to /
5. Django renders home page normally
6. User presses F5 (refresh)
7. Browser re-runs the GET request — no duplicate!
```

**In code:**
```python
def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias! We received your message.')
            return redirect('home')   # ← The "Redirect" in PRG
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()          # ← Empty form for GET requests

    return render(request, 'public_site/home.html', {'form': form})
```

### The Django Messages Framework

`messages.success(request, 'text')` stores a flash message in the session.  
It disappears after being displayed once. The base template renders them automatically:

```django
{% for message in messages %}
    <div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %}
```

Django maps message levels to Bootstrap alert colors:
- `messages.success` → `alert-success` (green)
- `messages.error` → `alert-danger` (red)
- `messages.warning` → `alert-warning` (yellow)
- `messages.info` → `alert-info` (blue)

---

## 🎨 Part 5: Templates — Rendering the Form {#part-5-templates}

### The Old Way (Static HTML)

The original template had hardcoded HTML inputs:
```html
<input type="text" class="form-control" id="name" required>
```

This worked visually, but had no connection to Django — errors couldn't be shown, CSRF wasn't included, and submission did nothing.

### The New Way (Django Template Tags)

```django
<form method="post" action="{% url 'home' %}#contact">
    {% csrf_token %}
    {% for field in form %}
    <div class="mb-3">
        <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
        {{ field }}
        {% if field.errors %}
            <div class="invalid-feedback d-block">{{ field.errors|join:", " }}</div>
        {% endif %}
    </div>
    {% endfor %}
    <button type="submit">Send</button>
</form>
```

#### What Each Tag Does

| Tag | Purpose |
|-----|---------|
| `{% csrf_token %}` | **Security** — inserts a hidden security token. Django rejects any POST without it. |
| `{% for field in form %}` | Loops over every field in `ContactForm` |
| `{{ field.label }}` | The human-readable field label (e.g., "Email Address") |
| `{{ field }}` | Renders the HTML `<input>` element with all your widget settings |
| `{{ field.id_for_label }}` | The `id` attribute Django gives the input (e.g., `id_email`) |
| `{{ field.errors }}` | List of validation errors for this field |
| `{{ field.errors\|join:", " }}` | Joins multiple errors with a comma |

### What is CSRF?

**CSRF** = Cross-Site Request Forgery. An attack where a malicious website tricks your browser into submitting a form to *your* site without you knowing.

Example: You're logged into your bank. A malicious site has:
```html
<form action="https://yourbank.com/transfer" method="post">
    <input name="amount" value="10000">
    <input name="to" value="hacker-account">
</form>
<script>document.forms[0].submit();</script>
```
If you visit that page while logged into your bank, it silently submits a transfer.

**Django's CSRF protection**: Every form includes a random token. Django verifies the token matches what it issued for your session. A foreign site can't know your token, so their form gets rejected with `403 Forbidden`.

**Never remove `{% csrf_token %}` from your forms.**

---

## 👨‍💼 Part 6: The Admin Panel — Free Superpower {#part-6-admin}

Django comes with a fully functional admin interface. Registering your model takes 3 lines of code and you get:
- List view with filters and search
- Create/edit/delete forms
- Pagination
- User permission control

**Our admin registration (`public_site/admin.py`):**
```python
@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event_type', 'submitted_at', 'is_read')
    list_filter = ('event_type', 'is_read')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)   # ← Can mark as read directly from the list!
```

To access it: `http://127.0.0.1:8000/admin/`

To create a superuser account:
```bash
python manage.py createsuperuser
```

---

## 🔁 The Full Request Lifecycle {#full-lifecycle}

```
Browser submits form (POST /  with form data)
            ↓
Django MIDDLEWARE
  - Check CSRF token          ← security
  - Load user session         ← who is this person?
            ↓
URL Router: path('', views.home)
            ↓
home() view executes:
  request.method == 'POST'    ← True
            ↓
  form = ContactForm(request.POST)
  form.is_valid()
    - EmailField validates email format
    - CharField checks max_length
    - Required fields checked
    - Returns True / False
            ↓
      True → form.save()
               ↓
             ORM translates to SQL:
             INSERT INTO public_site_bookingrequest (name, email, ...)
             VALUES ('José', 'jose@example.com', ...)
               ↓
             messages.success(...)
               ↓
             return redirect('home')
               ↓
             302 Response → browser follows to GET /
               ↓
             home() renders with success message
```

---

## 🐛 Common Mistakes & How to Fix Them {#common-mistakes}

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Forgot `{% csrf_token %}` | `403 Forbidden` on form submit | Add `{% csrf_token %}` inside the `<form>` tag |
| Forgot `makemigrations` | `OperationalError: no such table` | Run `python manage.py makemigrations` then `migrate` |
| Forgot `migrate` | Same error as above | Run `python manage.py migrate` |
| Rendering form before passing it in context | Empty form / template error | Make sure `context = {'form': form}` in your view |
| Rendering `{{ form }}` without `request.POST` | Form never shows errors | `form = ContactForm(request.POST)` not just `ContactForm()` |
| Not redirecting after POST | Duplicate submissions on refresh | Always `return redirect(...)` after a successful save |

---

## 🧠 Self-Assessment Questions {#self-assessment}

Test yourself after reading this guide:

1. **What's the difference between `forms.Form` and `forms.ModelForm`? When would you use each?**

2. **A user submits the form with an invalid email. What happens step by step?** (Trace the request lifecycle.)

3. **Why does Django reject a POST request that doesn't have a CSRF token?**

4. **What command do you run after adding a new field to a model? What does each command do?**

5. **What is the Post-Redirect-Get pattern and why does it prevent duplicate form submissions?**

6. **A booking was submitted but the admin can't see it. What are three possible reasons and how would you debug each?**

7. **What does `auto_now_add=True` do on a `DateTimeField`? How is it different from `auto_now=True`?**  
   *(Hint: one sets the time when the record is created, the other updates it every time the record is saved.)*

---

## 📚 Additional Resources

- [Django Forms Documentation](https://docs.djangoproject.com/en/5.2/topics/forms/)
- [Django ModelForms](https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/)
- [Django Admin Site](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)
- [CSRF Protection in Django](https://docs.djangoproject.com/en/5.2/ref/csrf/)
