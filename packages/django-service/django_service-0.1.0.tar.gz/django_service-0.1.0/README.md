# django-service [![PyPi license](https://img.shields.io/pypi/l/django-service.svg)](https://pypi.python.org/pypi/django-service)

[![PyPi status](https://img.shields.io/pypi/status/django-service.svg)](https://pypi.python.org/pypi/django-service)
[![PyPi version](https://img.shields.io/pypi/v/django-service.svg)](https://pypi.python.org/pypi/django-service)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-service.svg)](https://pypi.python.org/pypi/django-service)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-service.svg)](https://pypi.python.org/pypi/django-service)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-service.svg)](https://pypi.python.org/pypi/django-service)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-service.svg)](https://pypi.python.org/pypi/django-service)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-service.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-service.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-service/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-service?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-service/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-service/main) [![gitthub.com](https://github.com/DLRSP/django-service/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-service/actions/workflows/ci.yaml)

## Check Demo Project

- Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-service)

## Requirements

- Python 3.8+ supported.
- Django 4.2+ supported.

## Setup
1. Install from **pip**:
   ```shell
   pip install django-services
   ```
2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = (
       # ...
       "services",
       # ...
   )
   ```
3. Finally, modify your project `urls.py` with handlers for all errors:
   ```python
   # ...other imports...

   urlpatterns = [
       # ...other urls...
   ]
   ```
4. Execute Django's command `migrate` inside your project's root:
   ```shell
   python manage.py migrate
   Running migrations:
    Applying services.0001_initial... OK
   ```

## Run Example Project
```shell
git clone --depth=50 --branch=django-services https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
