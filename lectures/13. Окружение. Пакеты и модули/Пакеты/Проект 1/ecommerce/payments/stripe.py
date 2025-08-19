print(f"Загружается модуль `{__name__}`. Родительский пакет `{__package__}`")
from .utils import payments_utils_func
from ..utils import ecommerce_utils_func

def stripe_func():
    print("stripe_func called")
    payments_utils_func()
    ecommerce_utils_func()
    return "stripe"

def _private_stripe_func():
    print("_private_stripe_func called")
    return "_stripe"