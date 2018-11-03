__author__ = ["randomdude999","LappySheep"]
__copyright__ = "LSC"
__license__ = "MIT"
__version__ = "1.78c"

"""
Special Thanks
~~~~~~~~~~~~~~
-> randomdude999 (changing the code to a more effective set)
--> (also help with a lot of the concepts)
-> TheBloodlessMan (help with some of the concepts)


Newest Additions
~~~~~~~~~~~~~~~~
1.78c:
- Added lgv and lgf (log view, log file).
- Logs added to some processes.
1.78b:
- vwp issue partially fixed, might come back to this.
1.78:
- flt opcode modified so that it can run freely in a script rather than alone.
"""

import math
import decimal
Dec = decimal.Decimal
import functools
import string
import sys
from random import randint as RI
from random import choice as RC

subx,suby=0,0
constrFlag = ""
positions=[[],[]]
logs,logIndex=[],0

def _stop():
  stop=True
  print("Stopped.")

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

class InvalidVarName(ExecutionError):
    def __init__(self, varname):
        self.varname = varname
    def __str__(self):
        return f"Invalid variable name '{self.varname}'."

class InvalidFuncName(ExecutionError):
    def __init__(self, funcname):
        self.funcname = funcname
    def __str__(self):
        return f"Invalid function name '{self.funcname}'."

class InvalidFileName(ExecutionError):
    def __init__(self, filename):
        self.filename = filename
    def __str__(self):
        return f"Invalid file name '{self.filename}'."

class UndefinedVariable(ExecutionError):
    def __init__(self, varname):
        self.varname = varname
    def __str__(self):
        return f"Variable '{self.varname}' isn't defined."

class InvalidFlagChar(ExecutionError):
    def __init__(self, fcharname):
        self.fcharname = fcharname
    def __str__(self):
        return f"Flag character '{self.fcharname}' isn't defined."

def pop_stack(stack):
    try:
        return stack.pop()
    except IndexError:
        raise StackTooSmallError()

tern_ops = {
  "mdx": (lambda a,b,c: pow(a,b,c)),
}

def handle_ternop(op, s):
    c = pop_stack(s)
    b = pop_stack(s)
    a = pop_stack(s)
    s.append(tern_ops[op](a, b, c))

bin_ops = {
    "add": (lambda a,b: a+b),
    "sub": (lambda a,b: a-b),
    "mul": (lambda a,b: a*b),
    "div": (lambda a,b: a/b if b!=0 else Dec(0)),
    "fdiv": (lambda a,b: a//b if b!=0 else Dec(0)),
    #floor division
    "mod": (lambda a,b: a%b if b!=0 else Dec(0)),
    "gt": (lambda a,b: Dec(a>b)),
    "gte": (lambda a,b: Dec(a>=b)),
    "lt": (lambda a,b: Dec(a<b)),
    "lte": (lambda a,b: Dec(a<=b)),
    "eq": (lambda a,b: Dec(a==b)),
    "neq": (lambda a,b: Dec(a!=b)),
    "pow": (lambda a,b: a**b),
    "nrt": (lambda a,b: a**(1/b)),
    #n-th root
    "log": (lambda a,b: round(Dec(math.log(a,b))), 10),
    "gpw": (lambda a,b: round(Dec(math.log(a,b))), 10),
    # deprecated synonym
    "max": (lambda a,b: max(a,b)),
    "min": (lambda a,b: min(a,b)),
    "gin": (lambda a,b: Dec((str(a))[int(b)-1])),
    #get number from index position of larger number
}

def handle_binop(op, s):
    b = pop_stack(s)
    a = pop_stack(s)
    s.append(bin_ops[op](a, b))

unary_ops = {
    "sin": (lambda a: round(Dec(math.sin(math.radians(a))), 10)),
    "cos": (lambda a: round(Dec(math.cos(math.radians(a))), 10)),
    "tan": (lambda a: round(Dec(math.tan(math.radians(a))), 10) if a != 90 else Dec(0)),
    "acs": (lambda a: (round(Dec(math.acos(math.radians(a)))))if 1>a>-1else 0),
    "asn": (lambda a: (round(Dec(math.acos(math.radians(a)))))if 1>a>-1else 0),
    "rup": (lambda a: Dec(math.ceil(a))),
    "rdw": (lambda a: Dec(math.floor(a))),
    "inc": (lambda a: a+1),
    "dec": (lambda a: a-1),
    "neg": (lambda a: -a),
    "abs": (lambda a: abs(a)),
    "eq0": (lambda a: Dec(a == 0)),
    "neq0": (lambda a: Dec(a != 0)),
    "rec": (lambda a: Dec(1/a)),
    #reciprocal
    "sqrt": (lambda a: round(Dec(a**Dec(0.5)))),
    "cbrt": (lambda a: round(Dec(a**Dec(1/3)))),
    "adx": (lambda a: a+subx),
    "ady": (lambda a: a+suby),
    "dcd": (lambda a: Dec(RC((f"{a}")))),
    #random number from given number
    "src": (lambda a: (Dec(RI(0,a)))if a>-1else 0),
    #random number from 0 to a
    "nsrc": (lambda a: (Dec(RI(-a,0)))if a<1else 0),
    #random number from a to 0
    "msrc": (lambda a: Dec(RI(-a,a))),
    #random number from -a to a
    "fct": (lambda a: Dec(math.factorial(a)if a>=0else 0))
    #n factorial
}

def handle_unary_op(op, s):
    a = pop_stack(s)
    s.append(unary_ops[op](a))

def op_eu(s):
    s.append(round(Dec(math.e), 10)) # rounded to 10 places because i doubt people will need more

def op_pi(s):
    s.append(round(Dec(math.pi), 10))

def op_inp(s): #take input
    try:
      inp = Dec(input("<(Input)< "))
      s.append(inp)
    except decimal.InvalidOperation:
      s.append(0)

def op_dup(s): #double the top item on the stack
    a = pop_stack(s)
    s.append(a)
    s.append(a)

def op_out(s): #outputs + remove from stack
    a = pop_stack(s)
    print(str(a))

def op_fmc(s): #create code (rpn) file, q to quit
  a=input("<<FName< ")
  with open("{}.rpn".format(a),"w")as f:
    loop=True
    while loop==True:
      b=input("<Code< ")
      if b=="q":
        loop=False
        f.close()
      else:
        f.write(f"{b}\n")
        loop=True

def op_dsr(s): #define string, can be multi-line
  a=input("<<FName< ")
  with open("{}.txt".format(a),"w")as f:
    loop=True
    while loop==True:
      b=input("<String< ")
      if b=="q":
        loop=False
        f.close()
      else:
        f.write(f"{b}\n")
        loop=True

def op_flt(s): #load text file
  temp = pop_stack(s)
  c=True
  if temp[0] != "@":
    a=input("<<FName< ")
    s.append(temp)
  else:
    a=temp[1:]
    c=False
  try:
    with open("{}.txt".format(a),"r")as f:
      b=f.read()
      print(b)
      f.close()
      if c:
        main()
  except FileNotFoundError:
    if a[0] == ":":
      raise InvalidFileName(a[1:])
    else:
      raise InvalidFileName(a)

def op_flc(s): #trigger code file
  #note - to run freely, use jsr
  a=input("<<FName< ")
  try:
    with open("{}.rpn".format(a),"r")as f:
      b=f.readlines()
      for line in b:
        if line[0] == ";":continue
        try:
          cmd = line
          eval_cmd(cmd,variables)
        except (EOFError, KeyboardInterrupt):
          print()
          break
  except FileNotFoundError:
    if a[0] == ":":
      raise InvalidFileName(a[1:])
    else:
      raise InvalidFileName(a)

def op_cbs(s): #a b cbs - if a == 1, trigger a function
  b = pop_stack(s)
  a = pop_stack(s)
  if a == 1:
    if str(b)[0] == ":":
      try:
        with open("{}.rpn".format(b[1:]),"r")as f:
          c=f.readlines()
          for line in c:
            if line[0] == ";":continue
            try:
              cmd = line
              eval_cmd(cmd,variables)
            except (EOFError, KeyboardInterrupt):
              print()
              break
      except FileNotFoundError:
        if b[0] == ":":
          raise InvalidFileName(b[1:])
        else:
          raise InvalidFileName(b)
    else:
      s.append(b)
  else:
    s.append(b)
    s.append(a)

def op_cbe(s): #trigger function else trigger another/none
  c = pop_stack(s)
  b = pop_stack(s)
  a = pop_stack(s)
  if a == 1:
    if str(b)[0] == ":":
      try:
        with open("{}.rpn".format(b[1:]),"r")as f:
          g=f.readlines()
          for line in g:
            if line[0] == ";":continue
            try:
              cmd = line
              eval_cmd(cmd,variables)
            except (EOFError, KeyboardInterrupt):
              print()
              break
      except FileNotFoundError:
        if b[0] == ":":
          raise InvalidFileName(b[1:])
        else:
          raise InvalidFileName(b)
  
  elif a == 0:
    if str(c)[0] == ":":
      try:
        with open("{}.rpn".format(c[1:]),"r")as f:
          h=f.readlines()
          for line in h:
            if line[0] == ";":continue
            try:
              cmd = line
              eval_cmd(cmd,variables)
            except (EOFError, KeyboardInterrupt):
              print()
              break
      except FileNotFoundError:
          if c[0] == ":":
            raise InvalidFileName(c[1:])
          else:
            raise InvalidFileName(c)

    else:
      s.append(c)
      s.append(b)
  else:
    s.append(c)
    s.append(b)
    s.append(a)

def op_jsr(s): #jump to subroutine (function)
  a = pop_stack(s)
  if str(a)[0] == ":":
    try:
      with open("{}.rpn".format(a[1:]),"r")as f:
          b=f.readlines()
          for line in b:
            if line[0] == ";":continue
            try:
              cmd = line
              eval_cmd(cmd,variables)
            except (EOFError, KeyboardInterrupt):
              print()
              break
    except FileNotFoundError:
      raise InvalidFuncName(a[1:])
  else:
    s.append(a)

def op_pts(s): #if 1, print out the code of a function
  b = pop_stack(s)
  a = pop_stack(s)
  if a == 1:
    if str(b)[0] == ":":
      try:
        with open("{}.rpn".format(b[1:]),"r")as f:
          c=f.read()
          print(f">> {c}")
      except FileNotFoundError:
        raise InvalidFuncName(b[1:])
    else:
      s.append(b)
  else:
    s.append(b)
    s.append(a)

def op_pt2(s): #if 1, print the code of func a or b, or none
  c = pop_stack(s)
  b = pop_stack(s)
  a = pop_stack(s)
  if a == 1:
    if str(b)[0] == ":":
      try:
        with open("{}.rpn".format(b[1:]),"r")as f:
          g=f.read()
          print(f">> {g}")
      except FileNotFoundError:
        raise InvalidFuncName(b[1:])
  elif a == 0:
    try:
      with open("{}.rpn".format(c[1:]),"r")as f:
        h=f.read()
        print(f">> {h}")
    except FileNotFoundError:
      raise InvalidFuncName(c[1:])

def op_nop(s): #does literally nothing
  try:
    a = pop_stack(s)
    s.append(a)
  except:
    pass

def op_brk(s): #does "nothing"
  main() #... only if it is by itself
  #otherwise start over

def op_irp(s): #interrupt and ignore the next item
  try:
    a = pop_stack(s)
    del a
  except:
    pass

def op_swp(s): #swap the order of the 2 top stack items
  a = pop_stack(s)
  b = pop_stack(s)
  s.append(a)
  s.append(b)


def op_inx(s):
  global subx
  subx+=1

def op_dex(s):
  global subx
  subx-=1

def op_stx(s):
  global subx
  a=pop_stack(s)
  subx=a

def op_phx(s):
  global subx
  s.append(subx)

def op_otx(s):
  global subx
  print(f">>  {subx}")

def op_iny(s):
  global suby
  suby+=1

def op_dey(s):
  global suby
  suby-=1

def op_sty(s):
  global suby
  a=pop_stack(s)
  suby=a

def op_phy(s):
  global suby
  s.append(suby)

def op_oty(s):
  global suby
  print(f">>  {suby}")

def op_sxy(s):
  global subx,suby
  a,b=subx,suby
  suby=b
  subx=a
  del a,b


def op_ncr(s): #n choose r
  b = pop_stack(s)
  a = pop_stack(s)
  
  c = math.factorial(a)if a>=0else 0
  d = math.factorial(a-b)if (a-b)>=0else 0
  e = math.factorial(b)if b>=0else 0

  if d*e!=0:s.append(c/(d*e))

def op_npr(s): #n choose r * r!
  b = pop_stack(s)
  a = pop_stack(s)

  c = math.factorial(a)if a>=0 else 0
  d = math.factorial(a-b)if (a-b)>=0else 0

  if d!=0:s.append(c/d)


def op_mff(s): #make flag file
  inp = input("<Char+FName< ")
  with open("{}.rpnf".format(inp[1:]),"w")as f:
    f.write(inp[0])
    f.close()

def op_gff(s): #add flag file contents to flag variable
  global constrFlag
  inp = input("<FName< ")
  try: 
    with open("{}.rpnf".format(inp),"r")as f:
      char = f.read()
      constrFlag+=char
      f.close()
  except FileNotFoundError:
    raise InvalidFlagChar(inp)

def op_cfv(s): #reset flag
  global constrFlag
  constrFlag = ""

def op_outf(s): #print the flag
  global constrFlag
  print(constrFlag)if constrFlag !=""else print("Flag does not exist")


def op_trace(s): #basic stack tracing
  a = pop_stack(s)
  s.append(a)
  try:
    a+=0
    if int(a)==a:
      print("{}\nType: Integer".format(a))
    else:
      print("{}\nType: Float".format(a))
  except TypeError:
    if a[0]==":":
      try:
        with open("{}.rpn".format(a[1:]),"r")as f:
          b,d=[list(map(int,line.strip().split(' ')))for line in f],0
          for c in b:d+=len(c)
          print("{}\nType: Function, Exists\nItem Count:{}".format(a[1:],d))
      except FileNotFoundError:
        print("{}\nType: Function, Does Not Exist\nItem Count: N/A".format(a[1:]))
    else:
      print("{}\nType: Unidentified".format(a))
      

def op_adp(s): #add two positions (x,y)
  global positions
  b=pop_stack(s)
  a=pop_stack(s)
  positions[0].append(a)
  positions[1].append(b)

def op_vwp(s): #view two positions (x_n,y_n)
  global positions
  a=pop_stack(s)-1
  try:
    e=[row[int(a)] for row in positions]
    print(f"{e[0]}, {e[1]}")
  except IndexError:
    b=len(positions[0])
    c="are"if b!=1else"is"
    d="s"if b!=1else""
    print(f"There {c} only {b} set{d} of positions. {a+1} set(s) of positions cannot be loaded.")

def op_gtp(s): #get positions (x_n,y_n) and adds to stack
  global positions
  a=pop_stack(s)-1
  b=[row[int(a)] for row in positions]
  s.append(b[0])
  s.append(b[1])

def op_arp(s): #add positions (x_n,y_n) to (x_m,y_m)
  global positions
  b=pop_stack(s)-1
  a=pop_stack(s)-1
  c=[row[int(a)] for row in positions]
  d=[row[int(b)] for row in positions]
  for value in c:
    e=c.index(value)
    f,g=c[e-1]+d[e-1],c[e]+d[e]
  s.append(f)
  s.append(g)


def op_lgv(s): #view logs
  global logs
  out = ""
  for item in logs:
    out += f"{item}"
  print(out)

def op_lgf(s): #put logs in file
  global logs
  out = ""
  for item in logs:
    out += f"{item}"
  with open("logs.txt","w")as f:
    f.write(out)
    f.close()


ops = {
    "eu": op_eu,
    "pi": op_pi,
    "!inp": op_inp,
    "dup": op_dup,
    "self": op_dup,
    "!out": op_out,
    "dsr": op_dsr,
    "fmc": op_fmc,
    "flt": op_flt,
    "flc": op_flc,
    "cbs": op_cbs,
    "jsr": op_jsr,
    "nop": op_nop,
    "brk": op_brk,
    "irp": op_irp,
    "swp": op_swp,
    "inx": op_inx,
    "dex": op_dex,
    "stx": op_stx,
    "phx": op_phx,
    "otx": op_otx,
    "iny": op_iny,
    "dey": op_dey,
    "sty": op_sty,
    "phy": op_phy,
    "oty": op_oty,
    "sxy": op_sxy,
    "pts": op_pts,
    "cbe": op_cbe,
    "pt2": op_pt2,
    "ncr": op_ncr,
    "npr": op_npr,
    "mff": op_mff,
    "gff": op_gff,
    "cfv": op_cfv,
    "outf": op_outf,
    "!trace": op_trace,
    "adp": op_adp,
    "vwp": op_vwp,
    "gtp": op_gtp,
    "arp": op_arp,
    "lgv": op_lgv,
    "lgf": op_lgf,
    
}
# merge tern_ops into ops
for k, v in tern_ops.items():
    ops[k] = functools.partial(handle_ternop, k)
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

def eval_cmd(inp, variables):
    global logIndex
    temp = f"""Process {logIndex}: ~{inp}~\nVariables: {variables}\n\n"""
    logs.append(temp)
    logIndex+=1
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
            elif len(x) == 3 and x[0:2] in ("->", "<-", "--"):
                var_name = x[2]
                if var_name not in string.ascii_letters:
                    logs.append(f"Process {logIndex} failed\n\n")
                    raise InvalidVarName(var_name)
                if x[0:2] == "->":
                    variables[var_name] = pop_stack(stack)
                elif x[0:2] == "<-":
                    try:
                        stack.append(variables[var_name])
                        logs.append(f"Process {logIndex} - variable {var_name} set successfully")
                    except KeyError:
                        logs.append(f"Process {logIndex} failed\n\n")
                        raise UndefinedVariable(var_name)
                elif x[0:2] == "--":
                    try:
                        del variables[var_name]
                        logs.append(f"Process {logIndex} - variable {var_name} deleted successfully")
                    except KeyError:
                        logs.append(f"Process {logIndex} failed\n\n")
                        raise UndefinedVariable(var_name)
            elif x[0] == ":":
              stack.append(x)
            elif x[0] == "@":
              stack.append(x)
            else:
                logs.append(f"Process {logIndex} failed\n\n")
                raise InvalidOperation()
        except ExecutionError as e:
            logs.append(f"Process {logIndex} failed\n\n")
            print(f"Error occurred while evaluating token {x} (index {i}):")
            print(e)
            return

    if debug_mode:
            if stack:
                print(" ".join(str(x) for x in stack))
            print(f"Token count: {len(tokens)}")
            logs.append(f"Process {logIndex} - debug used")
    else:
        if stack:
            print(str(stack.pop()))
            logs.append(f"Process {logIndex} - last stack item returned")


def main():
    global variables
    variables = {}
    while True:
        try:
            cmd = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        eval_cmd(cmd, variables)

if __name__ == '__main__':
  with open("brk.rpn","w")as f:
    f.write("brk")
    f.close()
  main()
