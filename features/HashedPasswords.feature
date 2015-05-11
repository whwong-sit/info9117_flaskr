# Analysis:
#  If you want passwords to be hashed then the passwords in database
#  should be different from the actual passwords user input
#  and it should be hashed into the same value stored in database
#  when the user is logging in.
#
# Design Sketch:
#  * Passwords are stored in the database using values hashed by Flask-Bcrypt
#  * Passwords input by users when logging in will be hashed in the same manner then compare with the values in database
#  * If the hashed password that user input match with hashed password in database then user can log in successfully

Feature: HashedPasswords
	As an Administrator,
	I want passwords in the database to be stored in a digested form

  Scenario: Passwords in database is not plain text
    Given all the users and passwords in plain text
    When we compare them with passwords stored in database
    Then they should not be the same
	
  Scenario: Admin change password
    Given the admin is login
    When the admin changed a user password
    Then the user should not be able to log in with old password

  Scenario: User tries to login with hashed value
    Given the user knows the hashed value of their passwords
    When the user is trying to log in with hashed string
    Then the user should not be able to log in