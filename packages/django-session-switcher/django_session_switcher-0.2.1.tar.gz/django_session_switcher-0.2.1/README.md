# django-session-switcher

django-session-switcher allows you to quickly switch between dummy users. Handy tool to
create dummy content for your side projects from multiple users.

## Usage


1. Install the package
```
pip install django-session-switcher
```

2. Add `django_session_switcher` to your `INSTALLED_APPS` settings.

```
INSTALLED_APPS = [
    ...,
    "django_session_switcher",
]
```

3. Add the middleware to your project

```
MIDDLEWARE = [
    ...,
    "django_session_switcher.middleware.SessionSwitcherMiddleware",
]
```

4. Include the django_session_switchers URLconf in your project urls.py like this

```
path("__dss__/", include("django_session_switcher.urls")),
```

5. Run `python manage.py migrate` to create the models.

6. You need to add the dummy users to the django_session_switcher's `Session User` model. You
   can do this through django admin.

7. Once you have added some users to `Session User` you will be able to switch between
   added users with a single click.
