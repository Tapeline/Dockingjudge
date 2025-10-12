# Participation lifecycle

{{ decorated_definition("Contest session") }}

A contest session is started when used files an application for contest
participation (clicks `[Enter contest]` button). 

When contest session is started, if this <term:contest> is limited in time 
(i.e. `time_limit` is not -1), time countdown is started. After a defined
time limit, contest session ends.

While the contest session is active, user can view tasks and submit solutions
to them.

User cannot apply to a same contest twice.

A contest session cannot be ended forcibly.

When a contest is ended manually, all linked sessions are ended automatically.
