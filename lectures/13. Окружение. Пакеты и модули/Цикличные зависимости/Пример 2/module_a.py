import sys

print(
    f"Начало импорта А.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)

variable_a = "a"

def func_a():
    print("func_a запущен")
    import module_b
    print(module_b.variable_b)
    print("func_a завершен")

print(
    f"Конец импорта А.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)