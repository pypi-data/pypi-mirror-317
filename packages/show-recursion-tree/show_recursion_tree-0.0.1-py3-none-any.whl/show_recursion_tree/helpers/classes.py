from typing import Any, Optional

from colorama import Fore, Back

RESET_COLOR = Fore.RESET + Back.RESET

class Node:
    def __init__(self, val):
        self.val = val
        self.children = []

    def __str__(self):
        return f"Node({self.val})"

class Data:
    """
    contains shared data between recursive function calls
    """
    stack: list[Node] = []

    @classmethod
    def reset(cls):
        cls.stack = []

    @classmethod
    def push(cls, norm_args: str):
        newnode = Node(norm_args)
        
        if cls.stack:
            cls.stack[-1].children.append(newnode)

        cls.stack.append(newnode)

    @classmethod
    def pop(cls, func_output: Any):
        node = cls.stack.pop()
        # add func_output into node's val
        node.val = f"{node.val} => {func_output}"
        return node