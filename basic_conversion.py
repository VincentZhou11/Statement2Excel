import re
import json

op_not = "¬"
op_and = "∧"
op_or = "∨"
op_if = "→"
op_iff = "↔"
op_xor = "⊕"

test = "A_kni → (C_kna ↔ B_kni)"
test2 = test.replace(" ", "")
print(f"Test string: {test2}")

sample_map = {"A_kni":"a","A_kna":"b","B_kni":"c","B_kna":"d","C_kni":"e","C_kna":"f"}

symbols = re.compile(r"[∧∨→↔⊕]")
# Handle negations seperately because there only have one operand
neg_paranthesis = re.compile(r"^¬\(.*\)$") # ^ and $ makes sure that it is an exact match
neg_standalone = re.compile(r"^¬[^\s∧∨→↔⊕]*$")

def convert(op, opL, opR):
    if op==op_and:
        return (f"AND({opL}, {opR})")
    if op==op_or:
        return (f"OR({opL}, {opR})")
    if op==op_if:
        return (f"OR(NOT({opL}), {opR})")
    if op==op_iff:
        return (f"({opL}={opR})")
    if op==op_xor:
        return (f"(NOT({opL})={opR})")
    return None

def isWrapped(string):
    if not (string[0] == "(" and string[-1] == ")"):
        return False
    paranthesis = 0
    max_paran = 0
    groups = 0
    for i, char in enumerate(string):
        if char == "(":
            paranthesis += 1
        if char == ")":
            paranthesis -= 1
            groups +=1
        max_paran = max(paranthesis, max_paran)
    if groups > max_paran: # Paranthesis do not wrap around entire statement
        return False
    elif max_paran == 0: # No paranthesis
        return False
    else:
        return True

def recursion(string):
    # print(input)
    paranthesis=0
    while isWrapped(string):
        string = string[1:-1]
    # print(f"{input}: {neg_paranthesis.search(input) is not None or neg_standalone.search(input) is not None}")
    if neg_paranthesis.search(string) is not None or neg_standalone.search(string) is not None:
        return f"NOT({recursion(string[1:])})"
    for i, char in enumerate(string):
        if char == "(":
            paranthesis += 1
        if char == ")":
            paranthesis -= 1
        if paranthesis == 0 and symbols.search(char) is not None:
            opL = string[0:i]
            opR = string[i + 1:]
            return convert(char, recursion(opL), recursion(opR))
    return string

print(f"Test: {recursion(test2)}")

print(f"Symbols: ∧ ∨ → ↔ ⊕ ¬")
string = input("Column mapping: ")
mapping = json.loads(string)
print(mapping)

row = input("Input row #: ")

while (True):
    string = input("Input statement (type 'x' to exit): ")
    if string == "x":
        break
    output = recursion(string.replace(' ', ''))
    print(f"Raw Output: {output}")
    output2 = output
    for key in mapping.keys():
        output2 = output2.replace(key, mapping[key]+str(row))
    print(f"Output: {output2}")