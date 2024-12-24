
from src.show_recursion_tree import show_recursion_tree

@show_recursion_tree
def f(n):
    if n <= 4:
        return 1
    
    return f(n-4) + f(n-3) + f(n-2) + f(n-1)

f(7)