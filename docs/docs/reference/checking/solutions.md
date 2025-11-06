---
toc-depth: 3
---

# Solution types

## Quiz solutions

Quiz solutions are represented as a simple
text string that is checked in some way
[using quiz validators](../checking/quiz.md).


## Code solutions

Solutions to <term:code task|code tasks>
could be represented in one of following
formats:

### String solution

Solution is represented as a string — contents
of a single, main file of the solution.
Main file name is chosen automatically on
<term:Judgelet>'s behalf.

### Zip solution

Solution is represented as a Base64 string —
encoded zip and a main file name. This way
you can submit solutions that consist of
many files. This zip gets extracted on
<term:Judgelet>'s behalf and specified main file
is executed.
