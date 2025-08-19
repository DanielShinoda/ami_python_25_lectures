def crucial_func():
    print("Важная функция в работе")

def max(a: int, b: int):
    """Ловит даже на парковке"""
    if abs(a) > abs(b):
        return a, b
    else:
        return b, a
