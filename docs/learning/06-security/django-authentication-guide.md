# Django Authentication Deep Dive — Learning Guide
**How login, logout, sessions, and role-based access actually work**

*Author: Gerry Ochoa*  
*Date: April 22, 2026*  
*Sprint: Sprint 3, Phase 1*  
*Purpose: Educational resource — explains what we built, why, and how it works*

---

## 📚 Table of Contents

1. [Why Authentication Matters](#why-auth-matters)
2. [The Old System's Problem](#old-system-problem)
3. [Part 1: How Django Auth Works Under the Hood](#part-1-how-auth-works)
4. [Part 2: Building Login — Step by Step](#part-2-login)
5. [Part 3: Sessions — Staying Logged In](#part-3-sessions)
6. [Part 4: Logout — Why It Must Be a POST](#part-4-logout)
7. [Part 5: Protecting Views — @login_required](#part-5-protecting-views)
8. [Part 6: Role-Based Access Control](#part-6-rbac)
9. [Part 7: The Login Template](#part-7-template)
10. [Part 8: Settings That Connect It All](#part-8-settings)
11. [Authentication Flow Diagrams](#flow-diagrams)
12. [Common Mistakes](#common-mistakes)
13. [Self-Assessment Questions](#self-assessment)

---

## 🔐 Why Authentication Matters {#why-auth-matters}

Authentication answers the question: **"Who are you, and can I trust that?"**

Two related concepts:
- **Authentication**: Verifying identity ("You are José — I checked your password")
- **Authorization**: Determining permissions ("José can access the portal, but not the admin panel")

In our app, we need both:
- Only musicians and admins can enter the portal
- Only admins can manage users and booking requests

---

## ⚠️ The Old System's Problem {#old-system-problem}

The existing static mariachiweb site uses this authentication approach:

```javascript
// In musicians.js
function checkLogin() {
    const session = localStorage.getItem('mariachi_session');
    if (!session) {
        window.location.href = '/musicians/index.html';
        return false;
    }
    return true;
}
```

This stores the authentication state in `localStorage` — the browser's key-value storage. 

**The problem**: Anyone can bypass this from the browser console:
```javascript
localStorage.setItem('mariachi_session', JSON.stringify({
    user: 'hacker', role: 'admin', name: 'Fake Admin'
}));
```

Then they refresh the page and they're "logged in" as admin with no password.

**Django's approach**: The server decides who's authenticated. The browser only holds a session ID (a random string that means nothing by itself). The server maps that ID to a real user record in the database. You cannot forge a session ID because it's cryptographically random.

---

## 🧠 Part 1: How Django Auth Works Under the Hood {#part-1-how-auth-works}

### The Custom User Model

We set up a custom User model in Session 2 (`accounts/models.py`):

```python
class User(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    instrument = models.CharField(max_length=50, blank=True, null=True)
    # ...
```

`AbstractUser` gives us Django's built-in user fields for free:
- `username`, `email`, `first_name`, `last_name`
- `password` (stored as a **bcrypt hash**, never plain text)
- `is_staff`, `is_active`, `is_superuser`
- `date_joined`, `last_login`

We added our own fields on top: `role`, `instrument`, `phone`, `promo_opt_in`.

### Why `AUTH_USER_MODEL = 'accounts.User'` in Settings?

This tells Django: *use our custom User model, not the default one.*

**Critical**: This must be set **before your first migration**. Changing it later requires a complex migration and is a common source of headaches. We set it correctly from the beginning in Session 2.

---

## 🔑 Part 2: Building Login — Step by Step {#part-2-login}

### The View

```python
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.user.is_authenticated:
        return redirect('portal_dashboard')   # Already logged in

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)              # ← Create the session
            if user.role in ('musician', 'admin'):
                return redirect('portal_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'page_title': 'Login'})
```

### What `authenticate()` Does

`authenticate()` is Django's credential-checking function. It:
1. Looks up the user by username in the database
2. Verifies the password against the stored hash using bcrypt
3. Returns the `User` object if valid, or `None` if not

**Why use `authenticate()` instead of `User.objects.get(username=...)`?**

Because `authenticate()`:
- Uses bcrypt (a slow, one-way hashing algorithm) — you cannot reverse it
- Runs all registered authentication backends (important for future Google SSO)
- Calls `user.is_active` check automatically — disabled accounts are blocked

Never do this: ❌
```python
user = User.objects.get(username=username)
if user.password == password:   # WRONG — passwords are hashed!
```

### What `login()` Does

`login(request, user)` does two things:
1. Creates a **session** — stores the user's ID in the database session table
2. Sets a **session cookie** in the browser response (named `sessionid`)

The cookie contains only a random ID like `abc123xyz`. The actual user data stays on the server. On every subsequent request, the browser sends this cookie, Django looks up the session, and `request.user` becomes the logged-in user.

---

## 🍪 Part 3: Sessions — Staying Logged In {#part-3-sessions}

### How Sessions Work

```
LOGIN:
  1. User submits credentials
  2. Server validates, creates session record in DB:
     sessions table: { session_key: "abc123xyz", user_id: 5 }
  3. Server sends response with cookie:
     Set-Cookie: sessionid=abc123xyz; HttpOnly; SameSite=Lax

SUBSEQUENT REQUESTS:
  1. Browser automatically sends cookie:
     Cookie: sessionid=abc123xyz
  2. Django's SessionMiddleware reads the cookie
  3. Looks up "abc123xyz" in the sessions table
  4. Finds user_id=5
  5. Loads User object → request.user is now the logged-in user
```

### HttpOnly and SameSite

These are cookie security flags:
- **`HttpOnly`**: JavaScript **cannot** read this cookie. Protects against XSS attacks stealing the session.
- **`SameSite=Lax`**: The cookie is only sent on same-site requests. Protects against CSRF attacks.

Django sets both by default. You generally don't need to configure them manually.

---

## 🚪 Part 4: Logout — Why It Must Be a POST {#part-4-logout}

### The Logout View

```python
from django.contrib.auth import logout

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
```

`logout(request)` deletes the session record from the database and clears the cookie.

### Why Only POST?

Imagine if logout was a GET request, triggered by a URL like `/logout/`.

A malicious website could have:
```html
<img src="https://yoursite.com/logout/" width="1" height="1">
```

When you visit that page, your browser loads the invisible image, which sends a GET to `/logout/`, and **you're logged out without clicking anything**. This is a "logout CSRF" attack.

With POST-only logout:
- You need a `<form>` with `{% csrf_token %}`
- The CSRF token is unique to your session
- A foreign site cannot know your token
- You can only be logged out by intentionally clicking the logout button

**In the template:**
```html
<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

---

## 🛡️ Part 5: Protecting Views — @login_required {#part-5-protecting-views}

### The Decorator

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ...
```

`@login_required` is a **decorator** — a function that wraps another function to add behavior.

When a request comes in for a `@login_required` view:
1. Django checks `request.user.is_authenticated`
2. If `True` → run the view normally
3. If `False` → redirect to `settings.LOGIN_URL` (which we set to `'login'`)

Django also adds a `?next=/portal/` parameter to the redirect, so after logging in the user is sent back to where they were trying to go:
```
/login/?next=/portal/
```

Our login view currently ignores `next` — that's a Phase 2 improvement.

### How `settings.LOGIN_URL` Connects

```python
# settings.py
LOGIN_URL = 'login'                      # URL name for the login page
LOGIN_REDIRECT_URL = 'portal_dashboard'  # Where to go after login (if no 'next')
LOGOUT_REDIRECT_URL = 'home'             # Where to go after logout
```

`@login_required` reads `LOGIN_URL` to know where to redirect unauthenticated users.

---

## 👥 Part 6: Role-Based Access Control {#part-6-rbac}

### Two Layers of Protection

```python
@login_required                          # Layer 1: Must be logged in
def dashboard(request):
    if request.user.role not in ('musician', 'admin'):   # Layer 2: Must have right role
        raise PermissionDenied
    ...
```

**Why two layers?**

- `@login_required` blocks anonymous users → but customers can log in too
- The role check blocks customers who somehow have accounts

**`PermissionDenied`** raises an `HTTP 403 Forbidden` response.  
Django handles this automatically with a default 403 page (or a custom one if you create `templates/403.html`).

### Our Role Hierarchy

```
admin → Can do everything (portal + Django admin)
musician → Can access portal (scores, calendar, files)
customer → Can log in but not access portal (future: booking history)
```

The roles are enforced here:
```python
# In login_view:
if user.role in ('musician', 'admin'):
    return redirect('portal_dashboard')
return redirect('home')   # Customers land on home

# In dashboard view:
if request.user.role not in ('musician', 'admin'):
    raise PermissionDenied
```

### Checking Roles in Templates

The `user` object is available in every template automatically (Django's `auth` context processor adds it):

```django
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
    
    {% if user.role == 'admin' %}
        <a href="/admin/">Admin Panel</a>
    {% endif %}
    
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

---

## 🎨 Part 7: The Login Template {#part-7-template}

```django
<form method="post" action="{% url 'login' %}">
    {% csrf_token %}
    <input type="text" name="username" value="{{ request.POST.username|default:'' }}" autofocus>
    <input type="password" name="password">
    <button type="submit">Sign In</button>
</form>
```

### Key Details

**`name="username"` and `name="password"`** must match what the view reads:
```python
username = request.POST.get('username', '')
password = request.POST.get('password', '')
```

**`value="{{ request.POST.username|default:'' }}"`**  
When the form fails (wrong password), the username field stays filled in. The user doesn't have to retype it. The password is **not** re-filled for security reasons.

**`autofocus`**  
The browser automatically focuses this field when the page loads. Small UX improvement.

**We did NOT use a Django `Form` class for login.** Why?

Because the login form is so simple (just two text inputs) that a ModelForm would add complexity without benefit. We read `request.POST` directly. The more important validation happens in `authenticate()`.

---

## ⚙️ Part 8: Settings That Connect It All {#part-8-settings}

```python
# settings.py additions this session

AUTH_USER_MODEL = 'accounts.User'        # Custom user model (set in Session 2)
LOGIN_URL = 'login'                      # URL name for login page
LOGIN_REDIRECT_URL = 'portal_dashboard'  # Default redirect after login
LOGOUT_REDIRECT_URL = 'home'             # Default redirect after logout

# Email backend for development
# This prints emails to the terminal instead of sending them
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**For production**, the email backend changes to:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

All secrets go in `.env` (never committed to Git).

---

## 🔁 Authentication Flow Diagrams {#flow-diagrams}

### Login Flow
```
User visits /portal/
      ↓
@login_required checks is_authenticated
      ↓ NO
Redirect to /login/?next=/portal/
      ↓
User submits username + password
      ↓
authenticate(username, password)
      ↓ SUCCESS
login(request, user) → creates session
      ↓
Redirect to /portal/
      ↓
@login_required → is_authenticated? YES
      ↓
Role check: musician or admin? YES
      ↓
Dashboard renders ✅
```

### Session Verification on Every Request
```
Browser sends GET /portal/
    Cookie: sessionid=abc123xyz
          ↓
SessionMiddleware reads cookie
          ↓
Looks up "abc123xyz" in DB
          ↓
Finds user_id=5 (José)
          ↓
request.user = <User: jose>
          ↓
View executes with request.user available
```

---

## 🐛 Common Mistakes {#common-mistakes}

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Comparing `user.password` directly | Login never works | Use `authenticate()` |
| Logout via GET request | Logout CSRF vulnerability | Make logout a POST with CSRF token |
| Missing `@login_required` | Unauthenticated users see protected pages | Add decorator to every protected view |
| `AUTH_USER_MODEL` set after migrations | Migration conflicts | Must be set before first `migrate` |
| Forgetting role check | Customers can access musician portal | Check `user.role` after `@login_required` |
| No `next` handling in login | Users land on dashboard even when trying to access a specific page | Read `request.GET.get('next')` after login |

---

## 🧠 Self-Assessment Questions {#self-assessment}

1. **What is the difference between authentication and authorization? Give an example of each using our app.**

2. **How does `authenticate()` work? Why can't you compare `user.password == typed_password`?**

3. **What does `login(request, user)` actually do to the database and the browser?**

4. **A user is marked `is_active=False` by an admin. They try to log in with correct credentials. What happens and why?**

5. **Explain why logout must be a POST request, not a GET. Describe the attack that POST-only logout prevents.**

6. **What does `@login_required` do when an unauthenticated user visits `/portal/`? Trace the exact URL they end up on.**

7. **We have two layers of protection in `dashboard()`. Why isn't `@login_required` alone sufficient?**

8. **A musician logs in and the site redirects them to the home page instead of the portal. What's the most likely cause?**  
   *(Hint: look at the role check in `login_view`.)*

9. **How would you create a test musician account from the command line?**  
   *(Hint: `python manage.py createsuperuser` creates an admin, but how would you create a musician?)*

---

## 📚 Additional Resources

- [Django Authentication System](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [AbstractUser vs AbstractBaseUser](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/)
- [Django Sessions](https://docs.djangoproject.com/en/5.2/topics/http/sessions/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [bcrypt — Why slow hashing is good for passwords](https://auth0.com/blog/hashing-in-action-understanding-bcrypt/)
