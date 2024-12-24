# drf-addons-plus

**Some magic to the base Django REST Framework**

---

# Overview

This project provides some extra functionalities to be used with [Django REST Framework](https://www.django-rest-framework.org/)

* Field selection to Viewsets, eg. `?fields=id,name`
* Conditional filtering to Viewsets, eg. `?conditional=active,-inactive`

---

# Requirements

* Python 3.8+
* Django 4.2, 5.0, 5.1
* Django REST Framework 3.0+ ~or less, you can test it~

# Installation

Install using pip...
```sh
pip install drf_addons_plus
```

---

# Examples

* `models.py`:
```py
from django.db import models

class FooModel(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField()
    category = models.CharField(choices=['foo', 'bar'])
```

* `serializers.py`:
```py
from drf_addons_plus import serializers

from .models import FooModel


class FooSerializer(serializers.DynamicFieldsModelSerializer):
    class Meta:
        model = FooModel
        fields = ['name', 'status', 'category']
```

* `views.py`:
```py
from rest_framework import filters
from drf_addons_plus import filters as filters_plus
from drf_addons_plus import viewsets

from .models import FooModel
from .serializers import FooSerializer


class FooViewSet(viewsets.FieldsModelViewSet):
    queryset = FooModel.objects.all()
    serializer_class = FooSerializer
    permission_classes = []
    filter_backends = [filters.SearchFilter, filters_plus.ConditionalFilter, filters_plus.FieldsFitlter]
    search_fields = ['name']
    conditional_fields = ['status']
    filter_fields = ['category']
```


* Request `http://localhost:8000/foo/`:
```json
[
    {
        "name": "Bar",
        "status": false,
        "category": "Foo",
    }
]
```

* Request `http://localhost:8000/foo/?fields=name&conditional=-status`:
```json
[
    {
        "name": "Bar"
    }
]
```

* Request `http://localhost:8000/foo/?conditional=status`:
```json
[]
```

* Request `http://localhost:8000/foo/?category="foo"`:
```json
[
    {
        "name": "Bar",
        "status": false,
        "category": "Foo",
    }
]
```

---

## Disclaimer

This project has started and maybe will be maintened, but it's simple enough to probably not give you any trouble.

## Credits

[Django REST Framework](https://www.django-rest-framework.org)
[YAtOff](https://stackoverflow.com/a/23674297)
