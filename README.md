# django-panel-core
A bunch of libraries for building backend panel on django

# Installation
just `pip install -e git+https://github.com/ardzix/django-panel-core.git#egg=panel` in your python environment

#Usage

## Model lib
You can follow this example to create a model

```python
from django.db import models

# Create your models here.
from panel.libs.model import BaseModelGeneric

class TestField(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
```
