Feature: As an Administrator,
        I want to change user passwords dynamically.

  Scenario: Admin change password
    Given the Admin is logged in
    When the Admin goes to change password
    Then a changing password form is displayed

  Scenario: The user does not exist
    Given the Admin is logged in
    When the Admin goes to change password
    And the Username given does not exist
    Then the change should fail


  Scenario:user cannot use the old password to log in
    Given the user is logged in
    When the user login with old password
    Then user login should fail