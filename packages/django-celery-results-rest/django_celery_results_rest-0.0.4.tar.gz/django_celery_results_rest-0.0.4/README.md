django-celery-results RESTful API
==============================

RESTful API for django-celery-results.

# Usage

Add `celery_results_rest` in your project's `settings.py`:

```
INSTALLED_APPS = [
    'celery_results_rest',
]
```

Include `celery_results_rest.urls` in project's `urls.py`:

```
urlpatterns = [
    path('celery/results/', include('celery_results_rest.urls'))
]
```
