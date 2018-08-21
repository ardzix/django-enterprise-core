# django-panel-core
A bunch of libraries for building backend panel on django

# Installation
just `pip install -e git+https://github.com/ardzix/django-panel-core.git#egg=panel` in your python environment

# Libraries

## Model lib
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
