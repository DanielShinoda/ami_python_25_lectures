import sys

print(
    f"Начало импорта А.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)

import module_b

variable_a = "a"

def func_a():
    print(module_b.variable_b)

#print("variable_b from module_a:", module_b.variable_b)

print(
    f"Конец импорта А.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)