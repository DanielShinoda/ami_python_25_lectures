"""Email module docstring"""

print(f"Вызван модуль {__name__}")

def send_email(email_address: str, email_context: str):
    print(f"Отправлено письмо на адрес `{email_address}` c содержанием `{email_context}`")
