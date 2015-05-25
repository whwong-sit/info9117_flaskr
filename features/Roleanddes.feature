Feature: rolesanddes

  Scenario: Task Description
     Given the User is logged in
     When the user adds a new entry with task description
     Then Task Description will displayed

  Scenario: add new User Role, which is displayed on the show comments html
    Given the User is logged in
    When add the entry, the user would be able to assign user role to the entry
    Then the user role should be displayed on the comments page