Feature: page and task management

  Scenario: create text page
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
    When creates text page "Test text page"
    Then contest pages contain "Test text page"

  Scenario: change text page
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created text page "Test text page"
    When sets the page's text to "Hello, this is a test text"
    Then the page's text is now "Hello, this is a test text"

  Scenario: delete text page
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created text page "Test text page"
    When deletes the page
    Then contest pages do not contain "Test text page"


  Scenario: create quiz task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
    When creates quiz page "Test quiz page"
    Then contest pages contain "Test quiz page"

  Scenario: change quiz task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created text page "Test text page"
    When sets the page's points to 999
    Then the page's text is now 999

  Scenario: delete quiz task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created quiz page "Test quiz page"
    When deletes the page
    Then contest pages do not contain "Test quiz page"


  Scenario: create code task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
    When creates code page "Test code page"
    Then contest pages contain "Test code page"

  Scenario: change code task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created code page "Test code page"
    When sets the page's description to "**Some** __markdown__"
    Then the page's description is now "**Some** __markdown__"

  Scenario: delete code task
    Given registered user "Manager"
      And as user "Manager"
      And created contest "Test contest"
      And created code page "Test code page"
    When deletes the page
    Then contest pages do not contain "Test code page"
