print(f"Вызван модуль {__name__}")

TAX_COEF = 0.13
PUBLIC_COEF = 1
_PRIVATE_COEF = 0

def generate_tax(cash_amount: float):
    return cash_amount * TAX_COEF