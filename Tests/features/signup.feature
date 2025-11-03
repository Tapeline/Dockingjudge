Feature: signup
  Scenario: successful signup
    Given username "test_user", password "S0m3_H4rd_P455W0rd"
    When user signs up
    Then response contains "test_user"

  Scenario: username already taken
    Given registered user "test_user" "S0m3_H4rd_P455W0rd"
      And username "test_user", password "S0m3_H4rd_P455W0rd"
    When user signs up
    Then response contains "User with such name is already registered"
