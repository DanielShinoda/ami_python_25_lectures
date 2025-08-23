print(f"Загружается модуль `{__name__}`. Родительский пакет `{__package__}`")
from ecommerce.payments import *

print(paypal_func())
print(stripe_func())

#print(_private_paypal_func())