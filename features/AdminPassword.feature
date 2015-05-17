Feature: As an Administrator,
        I want to change user passwords dynamically.

  Scenario: Admin change password
    Given the Admin is logged in
    When the Admin goes to change password
    And admin change  a user password
    Then the password successfully changed

  Scenario: The user does not exist
    Given the Admin is logged in
    When the Admin goes to change password with invalid username
    Then the change should fail

  Scenario:user cannot use the old password to log in
    Given admin has changed a user password
    When the user login with old password
    Then user login should fail