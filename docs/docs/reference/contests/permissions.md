# Contest permissions

## Roles

In each <term:contest>, users are divided into two groups:

- <term:Contest participant|participants>

{{decorated_definition("Contest participant", "    ")}}

- <term:Contest manager|managers>
    
{{decorated_definition("Contest manager", "    ")}}

## View permissions

Any registered user is permitted to view <term:entry page>
and standings of a <term:contest>.

Any registered and [enrolled](./session.md) user can view all
<term:page|pages> of a contest.

## Solution permissions

Any registered and [enrolled](./session.md) user can submit <term:solution|solutions>
to all tasks as long as their <term:contest session|session> is active.

When session ends or contest ends, users cannot submit solutions.

Participants can view any solutions they own.

Managers can view any solutions of this contest.

!!! security
    Though through solution service's API it is only possible to view
    own <term:solution|solutions>, knowing a solution id user can access it directly
    from S3 storage, bypassing permission checks. It is a known security limitation.

    **Do not share your solution IDs and URLs during a contest.**

## Management permissions

Changing settings of a contest is only allowed to 
the <term:Contest manager|managers> of this contest.
