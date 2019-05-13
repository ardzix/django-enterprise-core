
# django-enterprise-core
A base core libraries and apps to build enterprise system using django

# Installation
just `pip install -e git+https://github.com/ardzix/django-enterprise-core.git#egg=enterprise` in your python environment

# Features

This repo contains work to build base structures of an enterprise system that includes:

### Notable libraries like:

- ProtectedMixin
  A library that handle your view permission based on django group of permission

- TrackerMixin
  A library that handle your visitor tracking in each view

- Rest Module base library
bunch of libraries that will useful if you want to build a rest api

### Base Apps that u will use in every development:

- Authentication
Don't worry about register, login, email verification etc. We handle it

- Tracker
App to track your visitor, a TrackerMixin viewer

- SuperUser
You want to manage another user inside your system? groups, permission, you name it. the super user app can handle it

### The Structures
Structure holds models and admins of django

- Authentication
- Common
- Integration
- Tracker

## Usage

* Insert desired app(s) to installed_apps in your settings.py

```python
    INSTALLED_APPS = [
        # ........
        'enterprise.apps.account',
        'enterprise.apps.superuser',
        # ........
    ]
```

* Include the app's url

```python
from django.contrib import admin
from django.conf.urls import url, include

from enterprise.apps.account import urls as account
from enterprise.apps.superuser import urls as superuser

urlpatterns = [
    # ...
    url(r'^account/', include((account, 'account'), namespace='account')),
    url(r'^superuser/', include((superuser, 'superuser'), namespace='superuser')),
    # ...
]
```

# Libraries

## Model lib

### First thing first

Insert path bellow to your settings.py
```python
    INSTALLED_APPS = [
        # ........
        'enterprise.structures.common',
        # ........
    ]
```

You can follow this example to create a model

```python
from django.db import models
from enterprise.libs.model import BaseModelGeneric

# Create your models here.
class TestField(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
```

## Protected Mixin
Protected mixin is a mixin for to protect view, it applies django permission and group to the implemented view

Just specify the namespace and model of the view

Example:
```python
from enterprise.libs.view import ProtectedMixin
from django.views.generic import TemplateView 

class UserView(ProtectedMixin, TemplateView):
    template_name = "account/user.html"
    namespace = "account"
    model = "user"

    def get(self, request):
        return self.render_to_response({})
```
