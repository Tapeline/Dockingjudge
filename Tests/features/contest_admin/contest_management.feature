Feature: contest management
  Scenario: create contest
    Given registered user "Manager"
      And as user "Manager"
    When creates contest "Test contest"
    Then response contains "Test contest"

  Scenario: change contest info
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
    When sets contest description "This is a test contest created in a scenario."
    Then response contains "This is a test contest created in a scenario."

  Scenario: delete contest
     Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
    When deletes contest
    Then response status "No content"
      And contest does not exist "Test contest"
