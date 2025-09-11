# How to solve tasks

## Short answer (quiz tasks)

These tasks only require you to input a single line of text as an answer.

They can score only 0 (if wrong) or full score (100, if right).

![](../img/ui-simple-task.png)

## Code tasks

These tasks require you to write a program, that will do the given task exactly as
written in the problem statement. Your solution will be tested against a number
test inputs. Some of them are visible to you, while others -- not. Your score
usually depends on how many tests you've passed. 

With the score, you'll receive **verdicts** small feedback about your solution.
If everything's ok, you'll receive `OK`. If your solution gave a wrong answer,
you'll get `WA`. If it has crashed while running, you'll get `RE` (runtime error).

Additionally, these tasks introduce **constraints**: memory (RAM) limit and time limit. 
If your solution exceeds these while running, it'll be stopped and you'll
receive `ML` (memory limit) or `TL` (time limit) verdict.

Also, the contest creators might set up **precompile checks**. E.g. forbid you to
import some modules. If your solution fails to comply, you'll receive `PCF`
(precompile check failed).

![](../img/ui-code-task.png)
