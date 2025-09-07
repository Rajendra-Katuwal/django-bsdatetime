# django_bsdatetime

[![PyPI version](https://badge.fury.io/py/django_bsdatetime.svg)](https://badge.fury.io/py/django_bsdatetime)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Django model fields for Bikram Sambat (Nepali) dates.

## Features

- ✅ Django model fields for BS dates and datetimes
- ✅ Stores Gregorian dates in database (for compatibility)
- ✅ Exposes Bikram Sambat interface in Python
- ✅ Full Django admin support
- ✅ Validation and error handling
- ✅ Built on the reliable `bsdatetime` core package

## Installation

```bash
pip install django_bsdatetime
```

This will automatically install the required `bsdatetime` core package.

## Django Setup

Add to your `INSTALLED_APPS` (optional, for static files):

```python
INSTALLED_APPS = [
    # ...
    'django_bsdatetime',
]
```

## Usage

```python
from django.db import models
from django_bsdatetime import BikramSambatDateField

class Person(models.Model):
    name = models.CharField(max_length=100)
    birth_date_bs = BikramSambatDateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - Born: {self.birth_date_bs}"

# Usage
person = Person.objects.create(
    name="राम बहादुर",
    birth_date_bs=(2050, 5, 15)  # BS date tuple
)

print(person.birth_date_bs)  # (2050, 5, 15)

# The actual database stores AD equivalent automatically
# But you work with BS dates in Python
```

## Available Fields

### `BikramSambatDateField`
- Stores date only
- Input/Output: `(year, month, day)` tuple
- Database storage: AD date

### `BikramSambatDateTimeField`  
- Stores date and time
- Input/Output: `(year, month, day, hour, minute, second)` tuple
- Database storage: AD datetime

## Field Aliases

For convenience and backward compatibility:
- `BSDateField` → `BikramSambatDateField`
- `NepaliDateField` → `BikramSambatDateField`

## Core Package

This package depends on [`bsdatetime`](https://pypi.org/project/bsdatetime/) for date conversion logic. You can use that package directly for non-Django projects:

```bash
pip install bsdatetime  # Core package only
```

## License

MIT
