# django-panel-core
A bunch of libraries for building backend panel on django

# Installation
just `pip install -e git+https://github.com/ardzix/django-enterprise-core.git#egg=panel` in your python environment

# Apps
Some apps included to handle basic functions on a django application, such as:

* **_Account_** app to handle authentication _(login, logout and change password)_
* **_Super User_** app to manage superuser administration _(users, groups and permissions)_

## Usage

* Insert desired app(s) to installed_apps in your settings.py

```python
    INSTALLED_APPS = [
        # ........
        'panel.apps.account',
        'panel.apps.superuser',
        # ........
    ]
```

* Include the app's url

```python
from django.contrib import admin
from django.conf.urls import url, include

from panel.apps.account import urls as account
from panel.apps.superuser import urls as superuser

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
        'panel.structures.common',
        # ........
    ]
```

You can follow this example to create a model

```python
from django.db import models
from panel.libs.model import BaseModelGeneric

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
from panel.libs.view import ProtectedMixin
from django.views.generic import TemplateView 

class UserView(ProtectedMixin, TemplateView):
    template_name = "account/user.html"
    namespace = "account"
    model = "user"

    def get(self, request):
        return self.render_to_response({})
```
