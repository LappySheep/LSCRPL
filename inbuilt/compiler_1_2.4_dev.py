import time
import math

class compileError(Exception):
  pass
class tooBig(Exception):
  pass
class alreadyExists(Exception):
  pass
class doesNotExist(Exception):
  pass

def notes():
  print("""
  Notes
  ~~~~~
  This is a big-endian compiler. Currently supports:
    a b add -> out(a+b)
    a b sub -> out(a-b)
    a b mul -> out(a*b)
    a b div -> out(a/b)
    (if b == 0, out(0) to avoid division by 0)
    a b fdiv -> out(a//b)
    (if b == 0, out(0) to avoid division by 0)
    a b mod -> out(remainder(a/b))
    (if b == 0, out(0) to avoid division by 0)
    eu -> replace item with Euler's number (32 d.p)
    pi -> replace item with pi (32 d.p)
    a b gt -> 1 if a>b else 0
    a b gte -> 1 if a>=b else 0
    a b lt -> 1 if a<b else 0
    a b lte -> 1 if a<=b else 0
    a b eq -> 1 if a==b else 0
    a b neq -> 1 if a!=b else 0
    a b pow -> out(a^b)
    a b nrt -> out(a^(1/b)); b-th root of a
    (b-root(a))
    a b gpw -> out x where b^x == a
    (log(base b,a) -> power x where x == answer)
    a sin -> out sin(x) - input == degrees
    a cos -> out cos(x) - input == degrees
    a tan -> out tan(x) - input == degrees
    (tan outputs 0 to the stack if the result is undefined)
    a rup -> returns a rounded up
    a rdw -> returns a rounded down
    (note - at 20 digits it may not round down anymore)
    a inc -> increments a
    a dec -> decrements a
    a neg -> negates the sign of a (pos->neg, neg->pos)
  """)
  time.sleep(0.5)
  main()

def exit():
  return

def lsc_abs(a):
  return abs(int(a))

def lsc_sin(a):
  return round(math.sin(math.radians(a)),8)

def lsc_cos(a):
  return round(math.cos(math.radians(a)),8)

def lsc_tan(a):
  if a==90:
    return 0
  else:
    return round(math.tan(math.radians(a)),8)

def lsc_up(a):
  return math.ceil(a)

def lsc_down(a):
  return math.floor(a)

def lsc_neg(a):
  return a*-1

ops = {
  #double operand opcodes below:
  "add":(lambda a,b:a+b),
  "sub":(lambda a,b:a-b),
  "mul":(lambda a,b:a*b),
  "div":(lambda a,b:a/b if b!=0 else 0),
  "fdiv":(lambda a,b:a//b if b!=0 else 0),
  "mod":(lambda a,b:a%b if b!=0 else 0),
  "abs":"",
  "eu":"",
  "pi":"",
  "gt":(lambda a,b:1if a>b else 0),
  "gte":(lambda a,b:1if a>=b else 0),
  "lt":(lambda a,b:1if a<b else 0),
  "lte":(lambda a,b:1if a<=b else 0),
  "eq":(lambda a,b:1if a==b else 0),
  "neq":(lambda a,b:1if a!=b else 0),
  "pow":(lambda a,b:a**b),
  "nrt":(lambda a,b:a**(1/b)),#outputs b-th root of a
  "gpw":(lambda a,b:math.log(a,b)),#b^return=a
  "sin":"",
  "cos":"",
  "tan":"",
  "rup":"",
  "rdw":"",
  "inc":"",
  "dec":"",
  "neg":"",
  "dup":"","self":""
}

other=["notes","exit"]

global variables
variables={}

def lscEval(exp):
  indiv=exp.split() #space-separated values -> list
  stack=[]

  for i, item in enumerate(indiv):
    if item=="eu":
      indiv[i]=math.e
    elif item=="pi":
      indiv[i]=math.pi

  for indi in indiv: #each item in the list
    if indi in ops: #check if available
      try:
        arg2=stack.pop()
        #stack reads closest from the opcode
        #therefore arg2 comes before arg1
        #else the answer will be flipped
      except:
        pass

      try:
        arg1=stack.pop()
        #thus arg1 is the first value
      except:
        pass

      #extra checks:
      if indi=="abs":
        ans=lsc_abs(arg2) #arg2 is the "first"
        #result that we have, so abs will sort this
        #out first.
      
      elif indi=="sin":
        ans=lsc_sin(arg2)
      
      elif indi=="cos":
        ans=lsc_cos(arg2)
      
      elif indi=="tan":
        ans=lsc_tan(arg2)
      
      elif indi=="rup":
        ans=lsc_up(arg2)
      
      elif indi=="rdw":
        ans=lsc_down(arg2)
      
      elif indi=="neg":
        ans=lsc_neg(arg2)
      
      elif indi=="inc":
        ans=arg2+1
      
      elif indi=="dec":
        ans=arg2-1
      
      elif indi=="dup" or indi=="self":
        ans=arg2
        secondary=True




      elif indi[:2]=="->":
        value=arg2 #value to store in variable
        var=indi[2:] #name of variable to store to
        if var in ops:
          raise alreadyExists("Sorry, {} already exists.".format(var))
        else:
          variables[var] = value

      elif indi[:2]=="<-":
        varName=indi[2:]
        if varName in variables:
          ans=variables[varName]
        else:
          raise doesNotExist("Sorry, {} does not exist.".format(varName))




      else:
        ans=ops[indi](arg1, arg2)
      #lambda functions above
      stack.append(ans)
      try:
        if secondary==True:
          stack.append(ans)
          secondary=False
      except:
        pass
      #push result to the stack
    else:
      try:
        stack.append(float(indi))
        #if integer...
      except:
        indiv.remove(indi)
        #...or if it's neither...?

  try:
    return stack.pop()
  except IndexError:
    return "Invalid state?"


def checks(a):
  #check for possible input
  if a.strip() in other:
    exec("{}()".format(a.strip()))
    #check if input is requesting anything different
  tempbool=False #var used...
  for x in a.split():
    if x not in ops:
      if x.replace(".","",1).isdigit()==False:
        tempbool=True #true = not in available opcodes

  for x in a.split():
    if x[:2]=="->"or x[:2]=="<-":
      tempbool=False

  if tempbool==True:
    print("Error found while compiling. Try again.")
    try:
      quit()
    except:
      raise compileError("""Error found while compiling:
      Invalid syntax (Unknown opcode or value?)""")
  try:
    b=lscEval(a)
  except:
    raise compileError("""Error found while compiling: Invalid syntax (Could not output result?)""")
  if len(str(b)) > 256:
    raise tooBig("""Error found while compiling:
    Result exceeds 256 characters""")
  return b


def main():
  a=input("<< ")
  b=checks(a)
  
  print(">> "+str(b))
  time.sleep(0.5)
  main()

main()
