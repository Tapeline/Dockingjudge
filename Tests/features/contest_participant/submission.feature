Feature: solution submission
  Scenario: successful quiz solution
    Given a contest with quiz task with right answer "1234"
      And registered user "Participant"
      And as user "Participant"
      And participates in contest
    When submits "1234" as solution to the quiz task
    Then solution's verdict is OK

  Scenario: wrong quiz solution
    Given a contest with quiz task with right answer "1234"
      And registered user "Participant"
      And as user "Participant"
      And participates in contest
    When submits "abcd" as solution to the quiz task
    Then solution's verdict is WA

  Scenario: successful code solution
    Given a contest with code task with test case (input "3" output "9")
      And registered user "Participant"
      And as user "Participant"
      And participates in contest
    When submits python "print(int(input())**2)" as solution to the code task
    Then solution's verdict is OK

  Scenario: wrong code solution
    Given a contest with code task with test case (input "3" output "9")
      And registered user "Participant"
      And as user "Participant"
      And participates in contest
    When submits python "print(input())" as solution to the code task
    Then solution's verdict is WA
