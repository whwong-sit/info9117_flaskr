# Analysis:
#  Admin can only change password for existing users
#  and user should not be able to log in with old passwords
#  once their passwords have been changed
#
# Design Sketch:
#  * Passwords are stored in the database table userPassword(username, password)
#  * Only admin can access the web page for changing password
#  * When admin is trying to change a password, the same password has to be input twice to confirm the change

Feature: AdminPasswords
	As an Administrator,
	I want to change user passwords dynamically

  Scenario: Only admin can change password
    Given a user is logged in
    When the user is trying to access change password
    Then the user should not be able to access it
    But once admin is logged in
    Then admin should be able to access change password
	
  Scenario: Admin change password
    Given a user can log in
    When admin is logged in
    And admin changes the password of this user
    Then the user should not be able to log in with stale password

  Scenario: User does not exist
    Given admin is logged in
    When admin is trying to change password for a non-existing user
    Then the change should fail