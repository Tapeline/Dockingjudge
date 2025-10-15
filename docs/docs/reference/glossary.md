---
hide-toc: true
---

# Term list

**term:Contest**
:   Contest is a collection of informational pages and tasks, available for solving under
    a limited (or not) time period, which users can participate in.


**term:Page**
:   A <term:quiz task>, a <term:code task> or a <term:text page>.


**term:Quiz task**
:   A task designed to be solved with a simple, 
    short answer (usually a line of text or a number).


**term:Code task**
:   A task designed to be solved by writing and submitting a valid
    program on one of the supported programming languages.


**term:Text page**
:   A page containing text info in Markdown format. Designed to provide
    help info, etc. 

    See also: <term:Entry page>


**term:Entry page**
:   A <term:text page> that is marked as entry page. Serves as a welcoming
    page and allows users to participate in contest (contest entrypoint).


**term:Contest session**
:   A span in time during which user is participating in a <term:contest> 
    and is allowed to solve tasks.


**term:Contest participant**
:   A user that participates in contest.


**term:Contest manager**
:   A user that created the contest and manages it.


**term:Submission**
:   An answer for a task that was submitted by user during their <term:contest session>.


**term:Solution**
:   Refers to <term:submission>.


**term:Verdict**
:   A short code telling status of a <term:submission>.

    See also: [List of verdicts](./checking/verdicts.md)


**term:Points**
:   An integer number, estimates how good a <term:solution> is and/or how did it
    pass <term:code task> <term:test case|test cases>.


**term:Test suite**
:   A collection of <term:test group|test groups>, 
    <term:precompile checker|precompile checkers>, and environment settings that is
    used to test and estimate <term:code task> <term:solution|solutions>.


**term:Test group**
:   A declared collection of <term:test case|test cases>,
    <term:test group dependency|test group dependencies>, a fixed maximum 
    <term:points> value and a <term:scoring policy> that describe how to test and estimate 
    <term:code task> <term:solution|solutions>.
    

**term:Scoring policy**
:   Describes how many points from maximum to score based on how successful test runs were.

    See also: [Test suite declaration](checking/code.md)


**term:Test case**
:   A collection of <term:test case validator|validators> and settings
    that describe environment of a single test <term:code task> <term:solution> run:
    what data to run with and how to check for right answer.


**term:Test case validator**
:   A declaration of how to check results of running a <term:code task> <term:solution>.


**term:Test group dependency**
:   Another <term:test group> in the same <term:test suite> which is required to
    be in state where all its <term:test case|test cases> pass in order to run
    this, dependent group.


**term:Precompile checker**
:   A declaration of how to check a <term:code task> <term:solution> source code before
    compiling and running.


**term:Judgelet**
:   An instance of an application that is used to run and test <term:code task> 
    <term:solution|solutions> in a safe, isolated environment.

    See also: [Judgelet service description](../services/judgelet/description.md)
