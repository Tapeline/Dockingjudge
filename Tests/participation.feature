Feature: contest participation

  Scenario: successful participation
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And set contest is_started True
      And registered user "Participant"
      And as user "Participant"
    When participates in contest
    Then response status "Created"
      And user "Participant" is a participant of the contest

  Scenario: cannot participate before start
    Given registered user "Participant"
      And as user "Participant"
      And created contest "Future contest" that starts in future
    When participates in contest
    Then response status "Forbidden"
      And response contains "Contest has not started yet"

  Scenario: cannot participate twice
    Given registered user "Participant"
      And as user "Participant"
      And created contest "Some contest"
      And participates in contest
    When participates in contest
    Then response status "Conflict"
      And response contains "User is already a participant"

  Scenario: cannot participate after end
    Given registered user "Participant"
      And as user "Participant"
      And created contest "Past contest" that has ended
    When participates in contest
    Then response status "Forbidden"
      And response contains "Contest has already ended"