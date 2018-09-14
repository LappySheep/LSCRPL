__author__ = "randomdude999"
__copyright__ = "LSC"
__credits__ = ["randomdude999", "LappySheep"]
__license__ = "MIT"
__version__ = "1.4"

import math
import decimal
Dec = decimal.Decimal
import functools

try:
    import readline
except ImportError:
    pass

class ExecutionError(Exception):
    pass

class StackTooSmallError(ExecutionError):
    def __str__(self):
        return "Not enough items on stack for this operation."

class InvalidOperation(ExecutionError):
    def __str__(self):
        return "Invalid instruction."

def pop_stack(stack):
    try:
        return stack.pop()
    except IndexError:
        raise StackTooSmallError()

bin_ops = {
    "add": (lambda a,b: a+b),
    "sub": (lambda a,b: a-b),
    "mul": (lambda a,b: a*b),
    "div": (lambda a,b: a/b if b!=0 else 0),
    "fdiv": (lambda a,b: a//b if b!=0 else 0),
    "mod": (lambda a,b: a%b if b!=0 else 0),
    "gt": (lambda a,b: Dec(a>b)),
    "gte": (lambda a,b: Dec(a>=b)),
    "lt": (lambda a,b: Dec(a<b)),
    "lte": (lambda a,b: Dec(a<=b)),
    "eq": (lambda a,b: Dec(a==b)),
    "neq": (lambda a,b: Dec(a!=b)),
    "pow": (lambda a,b: a**b),
    "nrt": (lambda a,b: a**(1/b)),
    "gpw": (lambda a,b: Dec(math.log(a,b))), #DEPRECATED
    "log": (lambda a,b: Dec(math.log(a,b))),
}

def handle_binop(op, s):
    b = pop_stack(s)
    a = pop_stack(s)
    s.append(bin_ops[op](a, b))

unary_ops = {
    "sin": (lambda a: round(Dec(math.sin(math.radians(a))), 10)),
    "cos": (lambda a: round(Dec(math.cos(math.radians(a))), 10)),
    "tan": (lambda a: round(Dec(math.tan(math.radians(a))), 10)),
    "rup": (lambda a: Dec(math.ceil(a))),
    "rdw": (lambda a: Dec(math.floor(a))),
    "inc": (lambda a: a+1),
    "dec": (lambda a: a-1),
    "neg": (lambda a: -a),
    "abs": (lambda a: abs(a)),
}

def handle_unary_op(op, s):
    a = pop_stack(s)
    s.append(unary_ops[op](a))

def op_eu(s):
    s.append(round(Dec(math.e), 10)) # rounded to 10 places because i doubt people will need more

def op_pi(s):
    s.append(round(Dec(math.pi), 10))

def op_dup(s):
    a = pop_stack(s)
    s.append(a)
    s.append(a)

ops = {
    "eu": op_eu,
    "pi": op_pi,
    "dup": op_dup,
    "self": op_dup,
}
# merge bin_ops into ops
for k, v in bin_ops.items():
    ops[k] = functools.partial(handle_binop, k)

# merge unary_ops into ops
for k, v in unary_ops.items():
    ops[k] = functools.partial(handle_unary_op, k)

def split_input(inp):
    # TODO: maybe make it possible to use non-space separators? i.e. "2 2add" is valid
    return inp.split()

def is_integer(x):
    try:
        float(x)
    except ValueError:
        return False
    # i really don't want to deal with these
    if "inf" in x.lower() or "nan" in x.lower():
        return False
    return True

def eval_cmd(inp):
    tokens = split_input(inp)
    stack = []
    debug_mode = False
    if tokens and tokens[0] == "dbg":
        debug_mode = True
        tokens = tokens[1:]

    for i, x in enumerate(tokens):
        try:
            if is_integer(x):
                stack.append(decimal.Decimal(x))
            elif x in ops:
                ops[x](stack) # the operator itself handles stack manipulation
            else:
                raise InvalidOperation()
        except ExecutionError as e:
            print(f"Error occurred while evaluating token {x} (index {i}):")
            print(e)
            return

    if debug_mode:
            if stack:
                print(" ".join(str(x) for x in stack))
            print(f"Token count: {len(tokens)}")
    else:
        if stack:
            print(str(stack.pop()))


def main():
    while True:
        try:
            cmd = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        eval_cmd(cmd)

if __name__ == '__main__':
    main()
