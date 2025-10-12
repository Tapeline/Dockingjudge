# Code solution types

Solutions to <term:code task|code tasks>
could be represented in one of following
formats:

## String solution

Solution is represented as a string — contents
of a single, main file of the solution.
Main file name is chosen automatically on
<term:Judgelet>'s behalf.

## Zip solution

Solution is represented as a Base64 string —
encoded zip and a main file name. This way
you can submit solutions that consist of
many files. This zip gets extracted on
Judgelet's behalf and specified main file
is executed.

