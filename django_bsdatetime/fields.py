"""Django model field implementations for Bikram Sambat dates.

These fields store values in Gregorian (AD) form at the database layer while
providing BS calendar semantics in Python code.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any
from django.db import models
from django.core.exceptions import ValidationError

try:
    import bsdatetime as bs

except ImportError as e:
    raise ImportError(
        "django-bikram-sambat requires 'bsdatetime'. Install with: pip install bsdatetime"
    ) from e


__all__ = [
    "BSDateField",
    "BSDateTimeField",
]

class BSDateField(models.DateField):
    """DateField that accepts and returns BS date tuples (year, month, day).

    Internally stored as a standard AD date in the database for portability.
    """

    description = "Bikram Sambat date"

    def to_python(self, value: Any):  # type: ignore[override]
        if value in (None, ""):
            return value
        if isinstance(value, tuple) and len(value) == 3:
            try:
                y, m, d = value
                if not all(isinstance(x, int) for x in [y, m, d]):
                    raise ValueError("BS date tuple components must be integers")
                return bs.bs_to_ad(y, m, d)
            except (ValueError, TypeError) as e:
                raise ValidationError(f"Invalid BS date tuple: {e}")
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            return value
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):  # type: ignore[override]
        if value is None:
            return value
        return bs.ad_to_bs(value)

    def get_prep_value(self, value):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and len(value) == 3:
            try:
                y, m, d = value
                if not all(isinstance(x, int) for x in [y, m, d]):
                    raise ValueError("BS date tuple components must be integers")
                return bs.bs_to_ad(y, m, d)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Unsupported value for BSDateField: {e}")
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            return value
        raise TypeError("Unsupported value for BSDateField")

    def value_to_string(self, obj):  # type: ignore[override]
        value = self.value_from_object(obj)
        if isinstance(value, tuple):
            y, m, d = value
            return f"{y:04d}-{m:02d}-{d:02d}"
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            y, m, d = bs.ad_to_bs(value)
            return f"{y:04d}-{m:02d}-{d:02d}"
        return ""


class BSDateTimeField(models.DateTimeField):
    """DateTimeField for BS calendar with tuple interface.

    Accepts (y,m,d,h,M,s) or (y,m,d) tuples and stores a naive datetime in AD.
    Returns (y,m,d,h,M,s) tuple from DB.
    """
    description = "Bikram Sambat datetime"

    def to_python(self, value: Any):  # type: ignore[override]
        if value in (None, ""):
            return value
        if isinstance(value, tuple) and (len(value) == 6 or len(value) == 3):
            try:
                if len(value) == 6:
                    y, m, d, h, M, s = value
                else:
                    y, m, d = value  # default midnight
                    h = M = s = 0
                ad_date = bs.bs_to_ad(y, m, d)
                return _dt.datetime(ad_date.year, ad_date.month, ad_date.day, h, M, s)
            except (ValueError, TypeError) as e:
                raise ValidationError(f"Invalid BS datetime tuple: {e}")
        if isinstance(value, _dt.datetime):
            return value
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):  # type: ignore[override]
        if value is None:
            return value
        if not isinstance(value, _dt.datetime):
            value = _dt.datetime.combine(value, _dt.time())
        y, m, d = bs.ad_to_bs(value.date())
        return (y, m, d, value.hour, value.minute, value.second)

    def get_prep_value(self, value):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and (len(value) == 6 or len(value) == 3):
            try:
                if len(value) == 6:
                    y, m, d, h, M, s = value
                else:
                    y, m, d = value
                    h = M = s = 0
                ad_date = bs.bs_to_ad(y, m, d)
                return _dt.datetime(ad_date.year, ad_date.month, ad_date.day, h, M, s)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Unsupported value for BSDateTimeField: {e}")
        if isinstance(value, _dt.datetime):
            return value
        raise TypeError("Unsupported value for BSDateTimeField")

    def value_to_string(self, obj):  # type: ignore[override]
        value = self.value_from_object(obj)
        if isinstance(value, tuple):
            y, m, d, *rest = value
            if len(rest) == 3:
                h, M, s = rest
            else:
                h = M = s = 0
            return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{M:02d}:{s:02d}"
        if isinstance(value, _dt.datetime):
            y, m, d = bs.ad_to_bs(value.date())
            return f"{y:04d}-{m:02d}-{d:02d} {value.hour:02d}:{value.minute:02d}:{value.second:02d}"
        return ""

