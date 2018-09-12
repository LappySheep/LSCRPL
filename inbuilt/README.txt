LSCRPL; LS' Challenges (server) Reverse Polish Language.

A slightly modified version of what is known as "reverse polish"; a stack based interpreter.
Previously this was pseudocode. As of 07/09/18 22:22, a compiler was created.


Available:
add
sub
mul
div
fdiv (floor divide; return quotient from division)
mod (return remainder from division)
abs (return absolute value of current state)
eu (Euler's number; avoid typing out the whole number - to 32 decimal places)
pi (pi; avoid typing out the whole number - to 32 decimal places)
gt (greater than)
gte (greater than or equal to)
lt (less than)
lte (less than or equal to)
eq (equal to)
neq (not equal to)
pow (power)
nrt (n-th root)
gpw (get power)
sin
cos
tan
rup (round up)
rdw (round down)
dup


Todo:

!out
outputs the current value on the stack

->store_val
example:
5 4 add 2 mul ->a
9 2 mul ->a
18 ->a

(variable a contains the number 18 now)

<-load_val
example:
5 4 add 2 mul ->a
<-a 5 add
>> 23

--del_val
5 4 add 2 mul ->a --a
<-a
(invalid opcode; a was removed)

:load_func
example:
:active <-a inc
(while program is active, a is incremented)

dfs - define function start
example:
"func" "a" dfs <-a 5 add !out dfe
(outputs a + 5)

dfe - define function end
see dfs

eq0 - returns 1 if value equals 0, otherwise returns 0

neq0 - returns 1 if value does not equal 0, otherwise returns 0
