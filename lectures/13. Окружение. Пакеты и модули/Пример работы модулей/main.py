import email_module as em
# Импортируем модуь email_module, но обращаться к нему будем через em
from report_module import *
# Импортировали всё из модуля report


print(f"Вызван модуль {__name__}")

tax_report = generate_tax_report(100) # используем функцию из repot_module

em.send_email("abc@ya.ru", tax_report) # через модуль email_module отправляем письмо

print(generate_tax(100)) # generate_tax из tax_module.py, доступ к которому получили через repot_module
print(f"PUBLIC_COEF = {pc}") # PUBLIC_COEF из tax_module.py, доступ к которому получили через repot_module

print(f"TAX_COEF = {_TAX_COEF}")
# к переменной _TAX_COEF из tax_module мы доступ не получили,
# т.к. сделали приватной переменную TAX_COEF в report_module
# а `from report_module import *` подтягивает только публичные объекты

print(f"PRIVATE_COEF = {_PRIVATE_COEF}")
# к переменной _PRIVATE_COEF из tax_module мы получаем доступ,
# несмотря на приватность переменной, т.к. мы явно импортировали её
# в report_module, и там же указали в атрибуте модуля __all__ наличие этой
# переменной. При импорте через * в таком случае будет импортировано всё, 
# что лежит в __all__