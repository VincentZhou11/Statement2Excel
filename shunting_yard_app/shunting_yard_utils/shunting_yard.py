# Code adapted from Tomek Korbak:
# https://tomekkorbak.com/2020/03/25/implementing-shunting-yard-parsing/
from dataclasses import dataclass
from typing import Optional, List

op_not = "¬"
op_and = "∧"
op_or = "∨"
op_if = "→"
op_iff = "↔"
op_xor = "⊕"

precedence = {
    f"{op_not}": 1,
    f"{op_and}": 2,
    f"{op_or}": 3,
    f"{op_if}": 4,
    f"{op_iff}": 5,
    f"{op_xor}": 5
}


@dataclass
class Node:
    symbol: str
    left: Optional['Node']
    right: Optional['Node']

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


@dataclass
class Tree:
    root: Node

    @classmethod
    def _tokenize(cls, text: str) -> List[str]:
        prev = ''
        tokenized = []
        for char in text:
            if prev.isalnum() and char.isalnum():
                tokenized.append(tokenized.pop() + char)
            else:
                tokenized.append(char)
            prev = char
        return tokenized

    @classmethod
    def has_precedence(cls, op1: str, op2: str) -> bool:
        precdence1 = precedence[op1]
        precdence2 = precedence[op2]
        return precdence1 < precdence2
    @classmethod
    def build(cls, text: str) -> 'Tree':
        operator_stack: List[str] = []
        operand_stack: List[Node] = []
        for char in cls._tokenize(text):
            # print(operator_stack, operand_stack, char)
            if char.isalnum():
                operand_stack.append(Node(symbol=char, left=None, right=None))
            elif len(operator_stack) > 0 and operator_stack[-1] == op_not and char in "∧∨→↔⊕":
                expression = operand_stack.pop()
                op = operator_stack.pop()
                operand_stack.append(Node(symbol=op, left=expression, right=None))
                operator_stack.append(char)
            # elif char in '+-' and len(operator_stack) > 0 and operator_stack[-1] in '*/':
            elif char in "∧∨→↔⊕" and len(operator_stack) > 0 and operator_stack[-1] in "∧∨→↔⊕" and cls.has_precedence(operator_stack[-1], char):
                right = operand_stack.pop()
                op = operator_stack.pop()
                left = operand_stack.pop()
                operand_stack.append(Node(symbol=op, left=left, right=right))
                operator_stack.append(char)
            elif char == ')':
                while len(operator_stack) > 0 and operator_stack[-1] != '(':
                    right = operand_stack.pop()
                    op = operator_stack.pop()
                    if op == op_not:
                        operand_stack.append(Node(symbol=op, left=right, right=None))
                    else:
                        left = operand_stack.pop()
                        operand_stack.append(Node(symbol=op, left=left, right=right))
                    # print(operator_stack, operand_stack)
                operator_stack.pop()
                # print(operator_stack, operand_stack)
            else:
                operator_stack.append(char)
        while len(operator_stack) > 0:
            # right = operand_stack.pop()
            # op = operator_stack.pop()
            # left = operand_stack.pop()
            # operand_stack.append(Node(symbol=op, left=left, right=right))
            right = operand_stack.pop()
            op = operator_stack.pop()
            if op == op_not:
                operand_stack.append(Node(symbol=op, left=right, right=None))
            else:
                left = operand_stack.pop()
                operand_stack.append(Node(symbol=op, left=left, right=right))
        # print(operator_stack, operand_stack)
        return cls(root=operand_stack.pop())

    def evaluate(self, node: Optional[Node] = None):
        OPS = {
            f"{op_not}": lambda x: f"NOT({x})",
            f"{op_and}": lambda x, y: f"AND({x},{y})",
            f"{op_or}": lambda x, y: f"OR({x},{y})",
            f"{op_if}": lambda x, y: f"OR(NOT({x}),{y})",
            f"{op_iff}": lambda x, y: f"({x}={y})",
            f"{op_xor}": lambda x, y: f"({x}=NOT({y}))"
        }
        node = node or self.root
        if node.is_leaf():
            return node.symbol
        elif node.symbol == op_not:
            return OPS[op_not](self.evaluate(node.left))
        else:
            op = OPS[node.symbol]
            return op(self.evaluate(node.left), self.evaluate(node.right))


def contains_unknown_characters(string: str):
    for char in string:
        if not(char.isalnum() or char in "∧∨→↔⊕¬_" or char.isspace()):
            print(char)
            print(ord(char))
            return True
    return False


def remove_unknown_characters(string: str):
    ret = ""
    for char in string:
        if char.isalnum() or char in "∧∨→↔⊕¬_":
            ret += char
    return ret


def do_mapping(mapping: dict, row:int, string:str):
    for key in mapping.keys():
        string = string.replace(key, mapping[key]+str(row))
    return string
