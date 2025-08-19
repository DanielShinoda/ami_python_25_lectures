import sys

print(
    f"Начало импорта B.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)

import module_a


variable_b = "b"

def func_b():
    print(module_a.variable_a)

#print("variable_b from module_a:", module_a.variable_a)

print(
    f"Конец импорта B.\nМодуль А в sys.modules: {'module_a' in sys.modules}"
    + f"\nМодуль B в sys.modules: {'module_b' in sys.modules}"
)