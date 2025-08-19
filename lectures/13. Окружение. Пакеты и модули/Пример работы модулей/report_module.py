from tax_module import (
    generate_tax,
    _PRIVATE_COEF,
    PUBLIC_COEF as pc, 
    TAX_COEF as _TAX_COEF
)

print(f"Вызван модуль {__name__}")


def generate_tax_report(cash_amount: float):
    tax_amount = generate_tax(cash_amount)
    return (
        f"Налог с суммы {cash_amount:.3f} составляет {tax_amount:.3f}."
        + f"Налоговый коэффициент = {_TAX_COEF}. Публичный коэффициент = {pc}"""
    )

__all__ = ['generate_tax', 'generate_tax_report', 'pc', '_PRIVATE_COEF']
