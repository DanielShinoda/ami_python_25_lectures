import sys

print(
    f"Начало импорта B.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)

variable_b = "b"

def func_a():
    print("func_b запущен")
    import module_a
    print(module_a.variable_a)
    print("func_b завершен")

print(
    f"Конец импорта B.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)