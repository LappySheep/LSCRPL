LSCRPL; LS' Challenges (server) Reverse Polish Language.

A slightly modified version of what is known as "reverse polish"; a stack based interpreter.
Previously this was pseudocode. As of 07/09/18 22:22, an interpreter was created.



Todo:

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
