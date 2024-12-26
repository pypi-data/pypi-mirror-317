# Pongjun Notes

**pongjun-notes** is a reusable Django app for managing notes.

---

## Installation

1. Install the package:
   ```bash
   pip install pongjun-notes
   ```

2. Add `'notes'` to `INSTALLED_APPS` in your `settings.py`:

   ```python
   INSTALLED_APPS = [
       'notes',
   ]
   ```

3. Include the `notes` URLs in your project's `urls.py`:

   ```python
   from django.urls import path, include

   urlpatterns = [
       path('notes/', include('notes.urls')),
   ]
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   
