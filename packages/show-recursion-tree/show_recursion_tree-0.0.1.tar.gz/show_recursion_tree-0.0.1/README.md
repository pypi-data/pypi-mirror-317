
# show_recursion_tree
prints out recursion tree

# Installation
```
pip install show_recursion_tree
```

# Example 1
```python
@show_recursion_tree
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))

"""
  (5,) => 120 
       |
  (4,) => 24
      |
 (3,) => 6
     |
 (2,) => 2
     |
(1,) => 1
"""
```

# Example 2
```python
from show_recursion_tree import show_recursion_tree

@show_recursion_tree
def fib(n):
    if n == 1:
        return 1
    if n == 2:
        return 1
    
    return fib(n-2) + fib(n-1)

print(fib(5))
"""
               __________________(5,) => 5___________________
               |                                            |
     ______(3,) => 2________                     ______(4,) => 3__________________
     |                     |                     |                               |
(1,) => 1             (2,) => 1             (2,) => 1                  ______(3,) => 2________
                                                                       |                     |
                                                                  (1,) => 1             (2,) => 1
"""
```

# Example 3
```python
@show_recursion_tree
def f(n):
    if n <= 4:
        return 1
    
    return f(n-4) + f(n-3) + f(n-2) + f(n-1)

f(7)

"""
     _____________________________________________(7,) => 13_______________________________________________
     |          |                               |                                                         |
(3,) => 1  (4,) => 1       _________________(5,) => 4_____________________          _________________(6,) => 7_________________________________
                           |          |                       |          |          |          |              |                               |
                      (1,) => 1  (2,) => 1               (3,) => 1  (4,) => 1  (2,) => 1  (3,) => 1      (4,) => 1       _________________(5,) => 4___________________
                                                                                                                         |          |                     |          |
                                                                                                                    (1,) => 1  (2,) => 1             (3,) => 1  (4,) => 1
"""
```