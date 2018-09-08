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


Todo:
dup - replicates the most recent item on the stack, ->store_val, <-load_val, pow, score - independant status holder, --del_val, :load_func, dfs - define function start, dfe - define function end, AddConversationMessage, ShowConversation, ClearConversation, DestroyConversation, ConversationShowing, ShowOpeningConversation, CloseOpeningConversation, eq0, neq0
