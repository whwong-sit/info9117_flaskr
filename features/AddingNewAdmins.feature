Feature: As an Administrator, I want to manage admin privileges of other users.

  Scenario: Adding new admin
    Given the Admin is logged in
    When the Admin grant admin privilege to an existing user
    Then the user become an admin successfully

  Scenario: The user does not exist
    Given the Admin is logged in
    When the Admin enters an invalid admin name
    Then the add fails

  Scenario:Revoke admin privilege from another admin
    Given the Admin is logged in
    When the admin is revoking privilege from a normal user
    Then the revoke fails
	But the admin is revoking privilege from another admin
	Then the revoke succeeds
