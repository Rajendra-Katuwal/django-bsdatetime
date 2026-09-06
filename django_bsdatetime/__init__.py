"""Django-bsdatetime integration package.

Provides Django model fields for Bikram Sambat dates, built on top of the
core bsdatetime package.
"""

__version__ = "1.2.1"

from .fields import (
    BSDateField,
    BSDateTimeField,
)

__all__ = [
    "__version__",
    "BSDateField",
    "BSDateTimeField",
]
