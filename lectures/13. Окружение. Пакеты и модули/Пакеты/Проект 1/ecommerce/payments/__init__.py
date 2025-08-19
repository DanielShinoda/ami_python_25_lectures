print(f"Загружается модуль `{__name__}`. Родительский пакет `{__package__}`")

from .paypal import *
from .stripe import *

__all__ = ("paypal_func", "stripe_func")
print(f"Загрузился модуль `{__name__}`. Родительский пакет `{__package__}`")
