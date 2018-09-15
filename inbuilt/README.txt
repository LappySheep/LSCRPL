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
eq0 (equal to 0)
neq0 (not equal to 0)
pow (power)
nrt (n-th root)
gpw (get power)
sin
cos
tan
rup (round up)
rdw (round down)
dup
->[letter] (e.g. ->a) (pop from stack and store to variable)
<-[letter] (e.g. <-a) (push the value of the varible on the stack)
--[letter] (e.g. --a) (delete the variable)

Todo:

!out
outputs the current value on the stack

Planned = Make a section where the interpreter generates files and uses stored data in those as opposed to having it stored in memory

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
