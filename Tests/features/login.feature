Feature: login
  Scenario: successful login
    Given registered user "test_user" "S0m3_H4rd_P455W0rd"
    When "test_user" "S0m3_H4rd_P455W0rd" logs in
    Then response contains "token"

  Scenario: invalid credentials
    Given registered user "test_user" "S0m3_H4rd_P455W0rd"
    When "test_user" "wrong password" logs in
    Then response contains "No active account found with the given credentials"
