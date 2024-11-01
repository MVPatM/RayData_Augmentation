This is the change part of albumentations library.
I push the these two functions to Compose class in albumentations/core/composition.py
These functions are Compose class's method.

- pushdown_float.py has the pushdown_float function that pushes down float operation to jitter or blur operation.
- reordering_operator.py has the reordering_operator function that operates crop, grayscale, resize operation firstly. 
