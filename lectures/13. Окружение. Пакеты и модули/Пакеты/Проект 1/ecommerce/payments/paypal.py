print(f"Загружается модуль `{__name__}`. Родительский пакет `{__package__}`")
import ecommerce.payments.utils as p_utils
import ecommerce.utils as e_utils

def paypal_func():
    print("paypal_func called")
    p_utils.payments_utils_func()
    e_utils.ecommerce_utils_func()
    return "paypal"

def _private_paypal_func():
    print("_private_paypal_func called")
    return "_paypal"