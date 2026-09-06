"""
Django model field implementations for Bikram Sambat dates.

These fields store values in Gregorian (AD) form at the database layer while
providing BS calendar semantics (via bsdatetime) in Python code.
"""

from __future__ import annotations

import datetime as _dt
from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

try:
    import bsdatetime as bs
except ImportError as e:
    raise ImportError(
        "django-bsdatetime requires 'bsdatetime'. "
        "Install with: pip install bsdatetime"
    ) from e


__all__ = [
    "BSDateField",
    "BSDateTimeField",
]

_DATE_STRING_FMT = "%Y-%m-%d"
_DATETIME_STRING_FMT = "%Y-%m-%d %H:%M:%S"


class BSDateField(models.DateField):
    """DateField that accepts and returns BS date tuples (year, month, day).

    Internally stored as a standard AD date in the database for portability.
    """

    description = "Bikram Sambat date"

    def to_python(self, value: Any):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and len(value) == 3:
            try:
                y, m, d = value
                if not all(isinstance(x, int) for x in (y, m, d)):
                    raise ValueError("BS date tuple components must be integers")
                return bs.bs_to_ad(y, m, d)
            except Exception as e:
                raise ValidationError(f"Invalid BS date tuple: {e}")
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            return value
        if isinstance(value, str):
            # Strings round-trip through value_to_string() in BS "%Y-%m-%d"
            # form, so they must be parsed as BS dates here too - not as
            # AD dates via the base DateField parser.
            try:
                y, m, d = bs.parse_bs_date(value, _DATE_STRING_FMT)
                return bs.bs_to_ad(y, m, d)
            except ValueError as e:
                raise ValidationError(f"Invalid BS date string: {e}")
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):  # type: ignore[override]
        if value is None:
            return None
        return bs.ad_to_bs(value)

    def get_prep_value(self, value):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and len(value) == 3:
            try:
                y, m, d = value
                return bs.bs_to_ad(y, m, d)
            except Exception as e:
                raise TypeError(f"Unsupported value for BSDateField: {e}")
        if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            return value
        if isinstance(value, str):
            # Mirrors to_python()'s string handling, so a raw string passed
            # straight to a query filter or save() (bypassing to_python) is
            # parsed as a BS date too, not rejected.
            try:
                y, m, d = bs.parse_bs_date(value, _DATE_STRING_FMT)
                return bs.bs_to_ad(y, m, d)
            except ValueError as e:
                raise TypeError(f"Invalid BS date string: {e}")
        raise TypeError("Unsupported value for BSDateField")

    def pre_save(self, model_instance, add):  # type: ignore[override]
        if self.auto_now or (self.auto_now_add and add):
            ad_value = _dt.date.today()
            # Keep the in-memory attribute consistent with what a fresh
            # from_db_value() read would return (a BS tuple), even though
            # the value actually persisted is the AD date below.
            setattr(model_instance, self.attname, bs.ad_to_bs(ad_value))
            return ad_value
        return super().pre_save(model_instance, add)

    def value_to_string(self, obj):  # type: ignore[override]
        value = self.value_from_object(obj)
        if isinstance(value, tuple):
            y, m, d = value
        elif isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
            y, m, d = bs.ad_to_bs(value)
        else:
            return ""
        return f"{y:04d}-{m:02d}-{d:02d}"


class BSDateTimeField(models.DateTimeField):
    """DateTimeField for BS calendar with tuple interface.

    Accepts (y,m,d,h,M,s) or (y,m,d) tuples and stores an AD datetime.
    Returns (y,m,d,h,M,s) tuple when reading from DB.
    """

    description = "Bikram Sambat datetime"

    def __init__(self, *args, auto_now: bool = False, auto_now_add: bool = False, **kwargs):
        if auto_now or auto_now_add:
            kwargs.pop("default", None)
            kwargs.setdefault("editable", False)
            kwargs.setdefault("blank", True)
        # auto_now/auto_now_add must be forwarded to DateTimeField.__init__ -
        # it sets self.auto_now/self.auto_now_add itself, and would silently
        # reset them back to False if they were only set here beforehand.
        super().__init__(*args, auto_now=auto_now, auto_now_add=auto_now_add, **kwargs)

    def _bs_tuple_to_ad_datetime(self, value: tuple) -> _dt.datetime:
        if len(value) == 6:
            y, m, d, h, M, s = value
        else:
            y, m, d = value
            h = M = s = 0
        ad_date = bs.bs_to_ad(y, m, d)
        dt = _dt.datetime(ad_date.year, ad_date.month, ad_date.day, h, M, s)
        if settings.USE_TZ:
            from django.utils import timezone
            dt = timezone.make_aware(dt, timezone.get_default_timezone())
        return dt

    def to_python(self, value: Any):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and (len(value) in (3, 6)):
            try:
                return self._bs_tuple_to_ad_datetime(value)
            except Exception as e:
                raise ValidationError(f"Invalid BS datetime tuple: {e}")
        if isinstance(value, _dt.datetime):
            return value
        if isinstance(value, str):
            # Strings round-trip through value_to_string() in BS
            # "%Y-%m-%d %H:%M:%S" form, so they must be parsed as BS
            # datetimes here too - not as AD datetimes via the base parser.
            try:
                y, m, d, h, M, s = bs.parse_bs_datetime(value, _DATETIME_STRING_FMT)
                return self._bs_tuple_to_ad_datetime((y, m, d, h, M, s))
            except ValueError as e:
                raise ValidationError(f"Invalid BS datetime string: {e}")
        return super().to_python(value)

    def pre_save(self, model_instance, add):  # type: ignore[override]
        from django.utils import timezone
        if self.auto_now or (self.auto_now_add and add):
            ad_value = timezone.now() if settings.USE_TZ else _dt.datetime.now()
            # Keep the in-memory attribute consistent with what a fresh
            # from_db_value() read would return (a BS tuple), even though
            # the value actually persisted is the AD datetime below.
            y, m, d = bs.ad_to_bs(ad_value.date())
            setattr(model_instance, self.attname, (y, m, d, ad_value.hour, ad_value.minute, ad_value.second))
            return ad_value
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now:
            kwargs["auto_now"] = True
        if self.auto_now_add:
            kwargs["auto_now_add"] = True
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):  # type: ignore[override]
        if value is None:
            return None
        if not isinstance(value, _dt.datetime):
            value = _dt.datetime.combine(value, _dt.time())
        y, m, d = bs.ad_to_bs(value.date())
        return (y, m, d, value.hour, value.minute, value.second)

    def get_prep_value(self, value):  # type: ignore[override]
        if value in (None, ""):
            return None
        if isinstance(value, tuple) and (len(value) in (3, 6)):
            try:
                return self._bs_tuple_to_ad_datetime(value)
            except Exception as e:
                raise TypeError(f"Unsupported value for BSDateTimeField: {e}")
        if isinstance(value, _dt.datetime):
            return value
        if isinstance(value, str):
            # Mirrors to_python()'s string handling, so a raw string passed
            # straight to a query filter or save() (bypassing to_python) is
            # parsed as a BS datetime too, not rejected.
            try:
                y, m, d, h, M, s = bs.parse_bs_datetime(value, _DATETIME_STRING_FMT)
                return self._bs_tuple_to_ad_datetime((y, m, d, h, M, s))
            except ValueError as e:
                raise TypeError(f"Invalid BS datetime string: {e}")
        raise TypeError("Unsupported value for BSDateTimeField")

    def value_to_string(self, obj):  # type: ignore[override]
        value = self.value_from_object(obj)
        if isinstance(value, tuple):
            y, m, d, *rest = value
            h, M, s = rest if len(rest) == 3 else (0, 0, 0)
        elif isinstance(value, _dt.datetime):
            y, m, d = bs.ad_to_bs(value.date())
            h, M, s = value.hour, value.minute, value.second
        else:
            return ""
        return f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{M:02d}:{s:02d}"
