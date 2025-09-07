# django-bsdatetime

Django model fields for Bikram Sambat (Nepali) dates built on the `bsdatetime` core.

Documentation: https://rajendra-katuwal.github.io/bsdatetime.docs/

## Install
```bash
pip install django-bsdatetime
```
Installs `bsdatetime` automatically.

## Quick model example
```python
from django.db import models
from django_bsdatetime import BikramSambatDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = BikramSambatDateField(null=True, blank=True)

person = Person.objects.create(name="राम बहादुर", birth_date_bs=(2050, 5, 15))
print(person.birth_date_bs)  # (2050, 5, 15)
```
Data is stored internally as Gregorian; you work with BS tuples.

## Provided fields
* BikramSambatDateField (aliases: BSDateField, NepaliDateField)
* BikramSambatDateTimeField

Input format:
* Date: (year, month, day)
* DateTime: (year, month, day, hour, minute, second)

## Why use it
* Clean separation of storage (AD) vs domain (BS)
* Validation & conversion handled in one place
* Admin friendly

Need pure functions only? Use core:
```bash
pip install bsdatetime
```

## License
MIT
