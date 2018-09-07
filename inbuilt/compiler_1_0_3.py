import time

class compileError(Exception):
  pass
class tooBig(Exception):
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
    a b fdiv -> out(a//b)
    a b mod -> out(remainder(a/b))
    eu -> replace item with Euler's number (32 d.p)
    pi -> replace item with pi (32 d.p)
  """)
  time.sleep(0.5)
  main()

def lsc_abs(a):
  return abs(int(a))

ops = {
  #double operand opcodes below:
  "add":(lambda a,b:a+b),
  "sub":(lambda a,b:a-b),
  "mul":(lambda a,b:a*b),
  "div":(lambda a,b:a/b),
  "fdiv":(lambda a,b:a//b),
  "mod":(lambda a,b:a%b),
  "abs":"",
  "eu":"",
  "pi":""
}

def lscEval(exp):
  indiv=exp.split() #space-separated values -> list
  stack=[]

  for item in indiv:
    if item=="eu":
      a=indiv.index(item)
      indiv[a]=2.71828182845904523536028747135266
    else:
      pass

  for item in indiv:
    if item=="pi":
      a=indiv.index(item)
      indiv[a]=3.14159265358979323846264338327950
    else:
      pass

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

      else:
        ans=ops[indi](arg1, arg2)
      #lambda functions above
      stack.append(ans)
      #push result to the stack
    else:
      try:
        stack.append(float(indi))
        #if integer...
      except:
        #...or if it's not an integer.
        stack.append(int(indi))

  return stack.pop()

def main():
  a=input("<< ")
  possible=["add","sub","mul","div","fdiv",
  "self","mod","abs","eu","pi",
  "0","1","2","3","4","5","6","7","8","9"]
  #check for possible input
  other=["notes"]
  if a in other:
    exec("{}()".format(a))
  #check if input is requesting anything different
  tempbool=False #var used...
  for x in a.split(" "):
    if x not in possible:
      tempbool=True #true = not in available opcodes
    else:
      tempbool=False #false = good stuff
  if tempbool==True:
    print("Error found while compiling. Try again.")
    try:
      quit()
    except:
      raise compileError("""Error found while compiling:
      Invalid syntax (Unknown opcode or value?)""")
  b=lscEval(a)
  if len(str(b)) > 256:
    raise tooBig("""Error found while compiling:
    Result exceeds 256 characters""")
    #prevent any problems that could occur
    #from having too many characters
    #(for whatever that could possibly happen)
  print(">> "+str(b))
  time.sleep(0.5)
  main()

main()
